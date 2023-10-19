using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ComponentModel;
using System.Windows;
using System.Windows.Input;

namespace MultipleDisplayScoreSoftware.ViewModels
{
    public class MainWindowViewModel
    {
        private readonly IScreenManager _screenManager;
        private int _numDisplays;
        public ICommand OpenNextWindowCommand { get; }

        public MainWindowViewModel(IScreenManager screenManager)
        {
            _screenManager = screenManager;
            _numDisplays = NumberOfDisplays();

            OpenNextWindowCommand = new RelayCommand(OpenNextWindow);
        }

        private void OpenNextWindow()
        {
            Window newWindow = new SecondaryWindow();
            _screenManager.ShowWindowOnNextScreen(newWindow);
        }


        public int NumDisplays
        {
            get => _numDisplays;
            set
            {
                _numDisplays = value;
                OnPropertyChanged(nameof(NumDisplays));
            }
        }

        public int NumberOfDisplays()
        {
            var totalScreens = _screenManager.GetTotalScreens();
            return totalScreens;
        }

        public IEnumerable<int> AvailableScreens
        {
            get
            {
                return Enumerable.Range(0, _screenManager.GetTotalScreens());
            }
        }

        public event PropertyChangedEventHandler? PropertyChanged;

        protected virtual void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }

    }
}
