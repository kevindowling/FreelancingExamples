// DI/ServiceLocator.cs
using Microsoft.Extensions.DependencyInjection;
using MultipleDisplayScoreSoftware.ViewModels;

public static class ServiceLocator
{
    public static ServiceProvider? ServiceProvider { get; private set; }

    public static void Configure()
    {
        var services = new ServiceCollection();
        services.AddSingleton<IScreenManager, ScreenManager>();
        services.AddTransient<MainWindowViewModel>();
        ServiceProvider = services.BuildServiceProvider();
    }
}
