//index.js
const app = getApp()

Page({
  onTapDayWeather(){
    wx.navigateTo({
      url: '/pages/list/list',
    })
  },//页面跳转至注册界面
  onTapToSignIn(){
    wx.navigateTo({
      url:'/pages/SignIn/SignIn',
    })
  }//页面跳转至登录界面
})
