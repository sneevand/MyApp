using System;
using Android.App;
using Android.Content.PM;
using Android.Runtime;
using Android.Views;
using Android.Widget;
using Android.OS;
using MyApp.Authentication;
using MyApp.Services;
using Android.Content;

namespace MyApp.Droid
{
    [Activity(Label = "MyApp", Icon = "@mipmap/icon", Theme = "@style/MainTheme", MainLauncher = true, ConfigurationChanges = ConfigChanges.ScreenSize | ConfigChanges.Orientation)]
    public class MainActivity : global::Xamarin.Forms.Platform.Android.FormsAppCompatActivity, IGoogleAuthenticationDelegate
    {
        // Need to be static because we need to access it in GoogleAuthInterceptor for continuation
        public static GoogleAuthenticator Auth;

        //protected override void OnCreate(Bundle savedInstanceState)
        //{
        //    TabLayoutResource = Resource.Layout.Tabbar;
        //    ToolbarResource = Resource.Layout.Toolbar;

        //    base.OnCreate(savedInstanceState);
        //    global::Xamarin.Forms.Forms.Init(this, savedInstanceState);
        //    LoadApplication(new App());

        //    Auth = new GoogleAuthenticator(Configuration.ClientId, Configuration.Scope, Configuration.RedirectUrl, this);

        //    var googleLoginButton = FindViewById<Button>(Resource.Id.googleLoginButton);
        //    googleLoginButton.Click += OnGoogleLoginButtonClicked;

        //}

        protected override void OnCreate(Bundle bundle)
        {
            base.OnCreate(bundle);

            SetContentView(Resource.Layout.Main);

            Auth = new GoogleAuthenticator(Configuration.ClientId, Configuration.Scope, Configuration.RedirectUrl, this);

            var googleLoginButton = FindViewById<Button>(Resource.Id.googleLoginButton);
            googleLoginButton.Click += OnGoogleLoginButtonClicked;
        }
        private void OnGoogleLoginButtonClicked(object sender, EventArgs e)
        {
            // Display the activity handling the authentication
            var authenticator = Auth.GetAuthenticator();
            var intent = authenticator.GetUI(this);
            Xamarin.Auth.CustomTabsConfiguration.CustomTabsClosingMessage = null;
            StartActivity(intent);
        }

        public async void OnAuthenticationCompleted(GoogleOAuthToken token)
        {
            var intent = new Intent(this, typeof(MainActivity));
            intent.SetFlags(ActivityFlags.ClearTop | ActivityFlags.SingleTop);
            StartActivity(intent);
            // Retrieve the user's email address
            var googleService = new GoogleService();
            var email = await googleService.GetEmailAsync(token.TokenType, token.AccessToken);

            // Display it on the UI
            var googleButton = FindViewById<Button>(Resource.Id.googleLoginButton);
            googleButton.Text = $"Connected with {email}";
            var emailstr = googleButton.Text;


            //SetContentView(Resource.Layout.DashboardView);
        }

        public void OnAuthenticationCanceled()
        {
            new AlertDialog.Builder(this)
                           .SetTitle("Authentication canceled")
                           .SetMessage("You didn't completed the authentication process")
                           .Show();
        }

        public void OnAuthenticationFailed(string message, Exception exception)
        {
            new AlertDialog.Builder(this)
                           .SetTitle(message)
                           .SetMessage(exception?.ToString())
                           .Show();
        }
    }
}