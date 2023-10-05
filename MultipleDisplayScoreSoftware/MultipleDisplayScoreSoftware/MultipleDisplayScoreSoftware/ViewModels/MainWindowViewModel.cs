using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MultipleDisplayScoreSoftware.ViewModels
{
    internal class MainWindowViewModel
    {
        private readonly IScreenManager _screenManager;

        public MainWindowViewModel(IScreenManager screenManager)
        {
            _screenManager = screenManager;
        }

        public int NumberOfDisplays()
        {
            return _screenManager.GetTotalScreens();
        }
       
    }
}
