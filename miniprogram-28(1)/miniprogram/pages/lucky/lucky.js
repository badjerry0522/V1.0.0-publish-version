//该页面是获取电影咨询页面
Page({
  data: {
    ctime:"empty",
    title:"empty",
    des:"empty",
    picUrl:"empty"
  },
  onLoad: function (options) {
    var _this=this;
    wx.request({//调用api获取最新的影视咨询
      url: 'https://api.tianapi.com/film/index?key=b24dd82f90421858834367d821d88b45&num=5', 
      success: function (res) {
        if(res.data.code == 200){
        _this.setData({
          ctime: res.data.newslist[0].ctime,
          title:res.data.newslist[0].title,
          des:res.data.newslist[0].description,
          picURL:res.data.newslist[0].picUrl
        })
        _this.data.content=res.data.newslist[0]
        console.log(res.data.newslist[0])
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