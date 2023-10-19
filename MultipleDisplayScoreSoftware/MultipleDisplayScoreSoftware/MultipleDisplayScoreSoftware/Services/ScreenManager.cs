using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Windows;
using System.Windows.Media;
using System.Management;

public interface IScreenManager
{
    void ShowWindowOnScreen(Window window, int screenIndex);
    void ShowWindowOnNextScreen(Window window);
    Window? GetWindowOnScreen(int screenIndex);
    int GetTotalScreens();
    void StartMonitoring();
    void StopMonitoring();
}
public class ScreenManager : IScreenManager
{
    [DllImport("user32.dll", SetLastError = true)]
    static extern bool EnumDisplayMonitors(IntPtr hdc, IntPtr lprcClip, EnumMonitorsDelegate lpfnEnum, IntPtr dwData);

    [StructLayout(LayoutKind.Sequential)]
    public struct Rect
    {
        public int left;
        public int top;
        public int right;
        public int bottom;
    }

    delegate bool EnumMonitorsDelegate(IntPtr hMonitor, IntPtr hdcMonitor, ref Rect lprcMonitor, IntPtr dwData);
    private List<DpiScale> monitorDpiList = new List<DpiScale>();

    private Dictionary<int, Window> screenWindowMap = new Dictionary<int, Window>();
    private List<Rect> monitorBoundsList = new List<Rect>();
    //Watches for monitor connection/disconnection events
    private ManagementEventWatcher? watcher;

    public ScreenManager()
    {
        EnumerateMonitors();
        StartMonitoring();
    }


    public void ShowWindowOnScreen(Window window, int screenIndex)
    {
        System.Diagnostics.Debug.WriteLine($"Trying to show window on screen: {screenIndex}");

        if (screenIndex < 0 || screenIndex >= monitorBoundsList.Count)
            throw new ArgumentOutOfRangeException(nameof(screenIndex));

        var screenBounds = monitorBoundsList[screenIndex];
        var dpiScale = monitorDpiList[screenIndex];

        window.Left = screenBounds.left / dpiScale.DpiScaleX;
        window.Top = screenBounds.top / dpiScale.DpiScaleY;

        // Set the window size to match the screen's size
        window.Width = (screenBounds.right - screenBounds.left) / dpiScale.DpiScaleX;
        window.Height = (screenBounds.bottom - screenBounds.top) / dpiScale.DpiScaleY;


       

        window.Show();
        screenWindowMap[screenIndex] = window;


    }



    public void ShowWindowOnNextScreen(Window window)
    {
        int nextScreenIndex = GetNextAvailableScreenIndex();
        ShowWindowOnScreen(window, nextScreenIndex);
    }

    private int GetNextAvailableScreenIndex()
    {
        for (int i = 2; i < monitorBoundsList.Count; i++)  // Start from screen index 2, assuming 0 is reserved for admin
        {
            if (!screenWindowMap.ContainsKey(i) || screenWindowMap[i] == null)
                return i;
        }

        // If all screens are occupied, start round robin from screen index 2
        return 2;
    }

    public Window? GetWindowOnScreen(int screenIndex)
    {
        screenWindowMap.TryGetValue(screenIndex, out Window? window);
        return window;
    }

    private void EnumerateMonitors()
    {
        EnumMonitorsDelegate del = new EnumMonitorsDelegate(MyMonitorEnumProc);
        bool success = EnumDisplayMonitors(IntPtr.Zero, IntPtr.Zero, del, IntPtr.Zero);
        if (!success)
        {
            int error = Marshal.GetLastWin32Error();
            Console.WriteLine($"Error {error} occurred while enumerating monitors.");
        }
    }

    private bool MyMonitorEnumProc(IntPtr hMonitor, IntPtr hdcMonitor, ref Rect lprcMonitor, IntPtr dwData)
    {
        monitorBoundsList.Add(lprcMonitor);

        // Assume a default DPI scale of 1.0 (96 DPI)
        DpiScale dpi = new DpiScale(1.0, 1.0);
        if (Application.Current.MainWindow != null)
        {
            // Get the DPI scale of the main window (assuming all monitors have the same DPI scale)
            dpi = VisualTreeHelper.GetDpi(Application.Current.MainWindow);
        }
        monitorDpiList.Add(dpi);

        return true;
    }

    public int GetTotalScreens()
    {
        return monitorBoundsList.Count;
    }

    public void StartMonitoring()
    {
        WqlEventQuery query = new WqlEventQuery(
            "SELECT * FROM Win32_DeviceChangeEvent WHERE EventType = 2 OR EventType = 3");
        watcher = new ManagementEventWatcher(query);
        watcher.EventArrived += new EventArrivedEventHandler(HandleMonitorEvent);
        watcher.Start();
    }

    private void HandleMonitorEvent(object sender, EventArrivedEventArgs e)
    {
        EnumerateMonitors();
    }

    public void StopMonitoring()
    {
        watcher?.Stop();
        watcher = null;
    }



}
