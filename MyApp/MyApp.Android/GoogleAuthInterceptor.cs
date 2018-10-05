using Android.App;
using Android.Content;
using Android.OS;
using System;

namespace MyApp.Droid
{
    [Activity(Label = "GoogleAuthInterceptor")]
    [
        IntentFilter
        (
            actions: new[] { Intent.ActionView },
            Categories = new[]
            {
                    Intent.CategoryDefault,
                    Intent.CategoryBrowsable
            },
            DataSchemes = new[]
            {
                // First part of the redirect url (Package name)
                "com.googleusercontent.apps.941140826447-rn9pb0hp7rkk27m7o8tqascj7vn1vb97"
            },
            DataPaths = new[]
            {
                // Second part of the redirect url (Path)
                "/oauth2redirect"
            }
        )
    ]
    public class GoogleAuthInterceptor : Activity
    {
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);

            Android.Net.Uri uri_android = Intent.Data;

            // Convert iOS NSUrl to C#/netxf/BCL System.Uri - common API
            Uri uri_netfx = new Uri(uri_android.ToString());
            
            // Send the URI to the Authenticator for continuation
            MainActivity.Auth?.OnPageLoading(uri_netfx);

            Finish();
        }
    }
}