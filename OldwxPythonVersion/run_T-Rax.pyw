import wx
from T_Rax_Controller import TraxMainViewController

app=wx.App(None)
TraxApp=TraxMainViewController()
#TraxApp.data.load_exp_data('test\\temper_F020.spe')
TraxApp.main_view.graph_panel.redraw_figure()
#main_view.data.load_ds_calib_data('binary files\\lamp_15_dn.SPE')
#main_view.data.load_us_calib_data('binary files\\lamp_15_up.SPE')
app.MainLoop()