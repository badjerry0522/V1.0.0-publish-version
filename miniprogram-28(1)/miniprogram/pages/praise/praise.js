//该页面是获取赞美页面
Page({
  data: {
    praise:""
  },
  onLoad: function (options) {
    var _this=this;
    wx.request({//调用api获取赞美言论
      url: 'https://api.tianapi.com/txapi/caihongpi/index?key=b24dd82f90421858834367d821d88b45', 
      success: function (res) {
        if(res.data.code == 200){
          console.log("200")
          _this.setData({
            praise: res.data.newslist[0].content
          })
      }else{
          _this.setData({
            praise: res.data.msg
          }) 
      }
      console.log(_this.praise)
      },
      fail: function (err) {
        console.log(err)
      }
    })
  },
})