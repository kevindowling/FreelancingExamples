using System;
using System.Collections;
using System.Collections.Generic;
using System.Configuration;
using System.Data;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using System;

namespace MultipleDisplayScoreSoftware
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {
        private readonly IHost _host;

        public App()
        {
            _host = new HostBuilder()
                .ConfigureServices((_, services) =>
                {
                    services.AddSingleton<IScreenManager, ScreenManager>();
                    // ... other services
                })
                .Build();
        }

        protected override void OnStartup(StartupEventArgs e)
        {
            var screenManager = _host.Services.GetRequiredService<IScreenManager>();
            // ... use screenManager or other services

            base.OnStartup(e);
        }

        protected override void OnExit(ExitEventArgs e)
        {
            _host.Dispose();
            base.OnExit(e);
        }
    }
}
