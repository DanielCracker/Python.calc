using System;
using System.Windows;
using System.Windows.Input;
using MahApps.Metro.Controls;
using Microsoft.Web.WebView2.Core.DevToolsProtocolExtension;
using System.Diagnostics;
using System.Text;
using System.Linq;
using System.Web;
using MahApps.Metro.Controls.Dialogs;
using static System.Net.Mime.MediaTypeNames;
using System.Windows.Navigation;

namespace WpfApp1
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    /// 

    public partial class MainWindow : MetroWindow
    {
        bool _isNavigating = false;
        public static RoutedCommand CallCDPMethodCommand = new RoutedCommand();
        DevToolsProtocolHelper _cdpHelper;
        DevToolsProtocolHelper cdpHelper;
        public void MetroWindow()
        {
            
            InitializeComponent();
            from_city.Text = "Москва";
            to_city.Text = "Москва";

        }

        public static readonly DependencyProperty MyPropertyProperty = DependencyProperty.Register(
    "MyProperty", typeof(string), typeof(MainWindow), new PropertyMetadata(default(string)));

        public string MyProperty
        {
            get { return (string)GetValue(MyPropertyProperty); }
            set { SetValue(MyPropertyProperty, value); }
        }



        #region GoogleMaps
        void GoToPageCmdCanExecute(object sender, CanExecuteRoutedEventArgs e)
        {
            e.CanExecute = webView != null && !_isNavigating;
        }

        async void GoToPageCmdExecuted(object target, ExecutedRoutedEventArgs e)
        {
            await webView.EnsureCoreWebView2Async();
            webView.CoreWebView2.Navigate((string)e.Parameter);
        }
        
        private void ConvertAddressToURL()
        {
            string? FromCity = from_city.Text;
            string? FromStreet = from_street.Text;
            string? FromHouse = from_house.Text;
            string? ToCity = to_city.Text;
            string? ToStreet = to_street.Text;
            string? ToHouse = to_house.Text;

            StringBuilder queryAddress = new StringBuilder();
            queryAddress.Append("https://www.google.com/maps?f=d&saddr=");

            if(FromStreet != String.Empty & ToStreet != string.Empty)
            {
                if (FromCity != String.Empty)
                {
                    queryAddress.Append(FromCity + "," + "+");
                }
                else
                {
                    queryAddress.Append("Москва" + "," + "+");
                }

                if (FromStreet != String.Empty)
                {
                    queryAddress.Append(FromStreet + "," + "+");
                }
                if (FromHouse != String.Empty)
                {
                    queryAddress.Append(FromHouse + "," + "+");
                }
                if (ToStreet != String.Empty)
                {
                    queryAddress.Append("&daddr=");
                }

                if (ToCity != String.Empty)
                {
                    queryAddress.Append(ToCity + "," + "+");
                }
                else
                {
                    queryAddress.Append("Москва" + "," + "+");
                }

                if (ToStreet != String.Empty)
                {
                    queryAddress.Append(ToStreet + "," + "+");
                }
                if (ToHouse != String.Empty)
                {
                    queryAddress.Append(ToHouse + "," + "+");
                }
            }
            queryAddress = queryAddress.Replace(" ", "+");
            queryAddress.Append("&dirflg=d");
            webView.Source = new Uri(queryAddress.ToString());
        }
        #endregion

        #region TextCHANGED
        private void from_city_TextChanged(object sender, System.Windows.Controls.TextChangedEventArgs e)
        {
            ConvertAddressToURL();
        }

        private void from_house_TextChanged(object sender, System.Windows.Controls.TextChangedEventArgs e)
        {
            ConvertAddressToURL();
        }

        private void from_street_TextChanged(object sender, System.Windows.Controls.TextChangedEventArgs e)
        {
            ConvertAddressToURL();
        }

        private void to_city_TextChanged(object sender, System.Windows.Controls.TextChangedEventArgs e)
        {
            ConvertAddressToURL();
        }

        private void to_street_TextChanged(object sender, System.Windows.Controls.TextChangedEventArgs e)
        {
            ConvertAddressToURL();
        }

        private void to_house_TextChanged(object sender, System.Windows.Controls.TextChangedEventArgs e)
        {
            ConvertAddressToURL();
        }
        #endregion

        #region CDP_COMMANDS
        async void ShowFPSCounter(object sender, RoutedEventArgs e)
        {
            await cdpHelper.Overlay.SetShowFPSCounterAsync(true);
        }

        async void HideFPSCounter(object sender, RoutedEventArgs e)
        {
            await cdpHelper.Overlay.SetShowFPSCounterAsync(false);
        }

        async void SetPageScaleTo4(object sender, RoutedEventArgs e)
        {
            await cdpHelper.Emulation.SetPageScaleFactorAsync(4);
        }

        async void ResetPageScale(object sender, RoutedEventArgs e)
        {
            await cdpHelper.Emulation.SetPageScaleFactorAsync(1);
        }

        async void ReloadPage(object sender, RoutedEventArgs e)
        {
            await cdpHelper.Page.ReloadAsync();
        }

        async void CaptureSnapshot(object sender, RoutedEventArgs e)
        {
            Trace.WriteLine(await cdpHelper.Page.CaptureSnapshotAsync());
        }

        async void GetAllCookies(object sender, RoutedEventArgs e)
        {
            Network.Cookie[] cookies = await cdpHelper.Network.GetAllCookiesAsync();
            StringBuilder cookieResult = new StringBuilder(cookies.Count() + " cookie(s) received\n");
            foreach (var cookie in cookies)
            {
                cookieResult.Append($"\n{cookie.Name} {cookie.Value} {(cookie.Session ? "[session cookie]" : cookie.Expires.ToString("G"))}");
            }
            MessageBox.Show(cookieResult.ToString(), "Cookies");
        }

        async void AddOrUpdateCookie(object target, RoutedEventArgs e)
        {
            bool cookie = await cdpHelper.Network.SetCookieAsync("CookieName", "CookieValue", null, "https://www.bing.com/");
            MessageBox.Show(cookie ? "Cookie is added/updated successfully" : "Error adding/updating cookie", "Cookies");
        }

        async void ClearAllCookies(object sender, RoutedEventArgs e)
        {
            await cdpHelper.Network.ClearBrowserCookiesAsync();
            MessageBox.Show("Browser cookies are deleted", "Cookies");
        }

        async void SetGeolocation(object sender, RoutedEventArgs e)
        {
            double latitude = 36.553085;
            double longitude = 103.97543;
            double accuracy = 1;
            await cdpHelper.Emulation.SetGeolocationOverrideAsync(latitude, longitude, accuracy);
            MessageBox.Show("Overridden the Geolocation Position", "Geolocation");
        }

        async void ClearGeolocation(object sender, RoutedEventArgs e)
        {
            await cdpHelper.Emulation.ClearGeolocationOverrideAsync();
            MessageBox.Show("Cleared overridden Geolocation Position", "Geolocation");
        }
        #endregion

        #region CDP_EVENTS
        async void SubscribeToDataReceived(object sender, RoutedEventArgs e)
        {
            await cdpHelper.Network.EnableAsync();
            cdpHelper.Network.DataReceived += PrintDataReceived;
            MessageBox.Show("Subscribed to DataReceived Event!", "DataReceived");
        }

        void UnsubscribeFromDataReceived(object sender, RoutedEventArgs e)
        {
            cdpHelper.Network.DataReceived -= PrintDataReceived;
            MessageBox.Show("Unsubscribed from DataReceived Event!", "DataReceived");
        }

        void PrintDataReceived(object sender, Network.DataReceivedEventArgs args)
        {
            Trace.WriteLine(String.Format("DataReceived Event Args - Timestamp: {0}   Request Id: {1}   DataLength: {2}", args.Timestamp, args.RequestId, args.DataLength));
        }

        async void SubscribeToAnimationCreated(object sender, RoutedEventArgs e)
        {
            await cdpHelper.Animation.EnableAsync();
            cdpHelper.Animation.AnimationCreated += PrintAnimationCreated;
            MessageBox.Show("Subscribed to AnimationCreated Event!", "AnimationCreated");
        }

        void UnsubscribeFromAnimationCreated(object sender, RoutedEventArgs e)
        {
            cdpHelper.Animation.AnimationCreated -= PrintAnimationCreated;
            MessageBox.Show("Unsubscribed from AnimationCreated Event!", "AnimationCreated");
        }

        void PrintAnimationCreated(object sender, Animation.AnimationCreatedEventArgs args)
        {
            Trace.WriteLine(String.Format("AnimationCreated Event Args - Id: {0}", args.Id));
        }

        async void SubscribeToDocumentUpdated(object sender, RoutedEventArgs e)
        {
            await cdpHelper.DOM.EnableAsync();
            cdpHelper.DOM.DocumentUpdated += PrintDocumentUpdated;
            MessageBox.Show("Subscribed to DocumentUpdated Event!", "DocumentUpdated");
        }

        void UnsubscribeFromDocumentUpdated(object sender, RoutedEventArgs e)
        {
            cdpHelper.DOM.DocumentUpdated -= PrintDocumentUpdated;
            MessageBox.Show("Unsubscribed from DocumentUpdated Event!", "DocumentUpdated");
        }

        void PrintDocumentUpdated(object sender, DOM.DocumentUpdatedEventArgs args)
        {
            Trace.WriteLine("DocumentUpdated Event Args - No Parameters", "DocumentUpdated");
        }

        async void SubscribeToDownloadWillBegin(object sender, RoutedEventArgs e)
        {
            await cdpHelper.Page.EnableAsync();
            cdpHelper.Page.DownloadWillBegin += PrintDownloadWillBegin;
            MessageBox.Show("Subscribed to DownloadWillBegin Event!", "DownloadWillBegin");
        }

        void UnsubscribeFromDownloadWillBegin(object sender, RoutedEventArgs e)
        {
            cdpHelper.Page.DownloadWillBegin -= PrintDownloadWillBegin;
            MessageBox.Show("Unsubscribed from DownloadWillBegin Event!", "DownloadWillBegin");
        }

        void PrintDownloadWillBegin(object sender, Page.DownloadWillBeginEventArgs args)
        {
            Trace.WriteLine(String.Format("DownloadWillBegin Event Args - FrameId: {0}   Guid: {1}   URL: {2}", args.FrameId, args.Guid, args.Url));
        }
        #endregion

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            from_city.Text = null;
            from_street.Text = null;
            from_house.Text = null;

            to_city.Text = null;
            to_street.Text = null;
            to_house.Text = null;

            from_floor.Value = from_floor.Minimum;
            to_floor.Value = to_floor.Minimum;

            from_elevator.IsOn = false;
            to_elevator.IsOn = false;

            to_from.IsOn = false;

            weight.Value = weight.Minimum;
            leight.Value = leight.Minimum;
            waiting.Value = waiting.Minimum;

            webView.Source = new Uri("https://www.google.com/maps/@55.7515132,37.6399222,12z");

        }

        private void from_city_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            from_city.Text = null;
            to_city.Text = null;
        }


         async void Whatsapp_Button_Click(object sender, RoutedEventArgs e)
        {
            webView.Visibility = Visibility.Hidden;
            whatsappView.Visibility = Visibility.Hidden;
            
            await theWindow.ShowMessageAsync("This is the title", "Some message");
            whatsappstab.IsSelected = true;
            whatsappView.Visibility=Visibility.Visible; 
            webView.Visibility = Visibility.Visible;
        }
    }
}
