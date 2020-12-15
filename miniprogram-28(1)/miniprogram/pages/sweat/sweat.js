//该页面是获取土味情话界面
Page({

  data: {
    content:"",
    
  },

  onLoad: function (options) {//调用api获取土味情话
    var _this=this;
    wx.request({
      url: 'https://api.tianapi.com/txapi/saylove/index?key=b24dd82f90421858834367d821d88b45', 
      success: function (res) {
        if(res.data.code == 200){
        _this.setData({
          content: res.data.newslist[0].content
        })
      }else{
          _this.setData({
            content: res.data.msg
          }) 
      }
      },
      fail: function (err) {
        console.log(err)
      }
    })
  },
  
})