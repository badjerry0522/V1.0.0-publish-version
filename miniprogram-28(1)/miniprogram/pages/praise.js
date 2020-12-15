
Page({
  data: {
    praise:""
  },
  onLoad: function (options) {
    console.log("praise begin")
    wx.request({
      url: 'https://api.tianapi.com/txapi/caihongpi/index?key=b24dd82f90421858834367d821d88b45', 
      success: function (res) {
        if(res.data.code == 200){
          console.log("200")
          that.setData({
            praise: res.data.newslist[0].content
          })
      }else{
          that.setData({
            praise: res.data.msg
          }) 
      }
      console.log(this.praise)
      },
      fail: function (err) {
        console.log(err)
      }
    })
  },
})