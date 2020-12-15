//此页面是匹配页面
const app=getApp();
const db=wx.cloud.database();
Page({
  onLoad:function(options){
    console.log(app.globalData.userid);
  },
  data:{
    constellation:'',
    Url:'https://api.tianapi.com/txapi/xingzuo/index?key=b24dd82f90421858834367d821d88b45&me=',
    gender:"",
    usernumber:-1,
    anotheruser_NO:-1,
    anotheruser_id:"empty",
    PN:"",
    wxID:"",
    name:"",
    cons:"",
    anotheruser_constellation:"金牛",
    idea:"",
    text1:"",
    text2:"",
    text3:"",
  },
  start_matching:function(e){//点击开始匹配按钮
    var _this=this;
    wx.cloud.callFunction({//在数据库中获取当前用户的id
      name:"search",
      data:{
        tag:app.globalData.userid
      },
      success:function(res){
        _this.data.constellation=res.result.data[0].dbuserinf.constellation
        _this.data.Url=_this.data.Url+_this.data.constellation
        _this.data.gender=res.result.data[0].dbuserinf.gender
        _this.data.usernumber=res.result.data[0].userNO
        console.log(_this.data.usernumber)
      }
    })


    
    db.collection('num_user').where({tag:"number_user"}).get({//通过当前用户的id在数据库中查找当前用户的信息
      success:function(res){

        _this.data.anotheruser_NO=Math.ceil((Math.random()*10000000)%res.data[0].number)
        while(_this.data.usernumber==_this.data.anotheruser_NO) _this.data.anotheruser_NO=Math.ceil((Math.random()*10000000)%res.data[0].number)//随机获取其他人的用户id号码，进行匹配


        db.collection('1127').where({userNO:_this.data.anotheruser_NO}).get({//通过其他人的用户id在数据库中查找其他人的用户信息，并显示在屏幕上
          success:function(res){
            console.log("found")
            console.log(res)
            _this.setData({
              PN:res.data[0].dbuserinf.phnum,
              wxID:res.data[0].dbuserinf.wxid,
              name:res.data[0].dbuserinf.name,
              cons:res.data[0].dbuserinf.constellation,
              gender:res.data[0].dbuserinf.gender,
              idea:res.data[0].dbuserinf.idea,
            })
            _this.data.anotheruser_constellation=res.data[0].dbuserinf.constellation
            console.log(res.data[0].dbuserinf.phnum)
            console.log(res.data[0].dbuserinf.wxid)
          }
        })
      }
    })
    wx.request({//调用星座匹配api
     url:'https://api.tianapi.com/txapi/xingzuo/index?key=b24dd82f90421858834367d821d88b45&me='+_this.data.constellation+'&he='+_this.data.anotheruser_constellation, 
      success: function (res) {
        if(res.data.code == 200){
          _this.setData({
            text1:res.data.newslist[0].title,
            text2:res.data.newslist[0].grade,
            text3:res.data.newslist[0].content
          })
        }
        else{
          if(res.data.msg=='数据返回为空'){
            _this.setData({
              PN:"请重新匹配",
              wxID:"请重新匹配",
            })
          }
        }
      },
      fail: function (err) {
        console.log(err)
      }
    })
  },
  getpraise:function(e){
    wx.navigateTo({
      url: '/pages/praise/praise',//跳转至获取赞美的页面
    })
  },
  dogdiary:function(e){
    wx.navigateTo({
      url: '/pages/lip/lip',//跳转至获取舔狗日记界面
    })
  },
  pyq:function(e){
    wx.navigateTo({
      url: '/pages/lisa/lisa',//跳转至获取pyq文案界面
    })
  },
  lucky:function(e){
    wx.navigateTo({
      url: '/pages/lucky/lucky',//跳转至获取电影咨询界面
    })
  },
  sweat:function(e){
    wx.navigateTo({
      url: '/pages/sweat/sweat',//跳转至获取土味情话界面
    })
  }
})