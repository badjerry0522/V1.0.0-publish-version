//此页面是登录界面
const db=wx.cloud.database();
const app=getApp();
Page({

  data: {
    userid:"empty",
    userpwd:"empty"
  },
  input_id:function(e){
    this.data.userid=e.detail.value;//获取用户id
  },
  input_pwd:function(e){
    this.data.userpwd=e.detail.value;//获取用户密码
  },
  tap_submit:function(e){
    var _this=this

    db.collection('1127').where({//在数据库中查找输入的用户id
      userid:_this.data.userid
    }).get({
      success :function(res){
        if(typeof(res.data[0])=="undefined"){//如果为查找到相应的用户id
          console.log("not found")
          wx.showToast({
            title:"id not establish",
            icon:'none',
            duration:2000
          })
        }
        else{//查找到输入的用户id
          if(res.data[0].userpwd!=_this.data.userpwd){//该用户的密码不匹配
            wx.showToast({
              title:"wrong pwd",
              icon:"none",
              duration:2000
            })
          }
          else{//该用户的密码匹配//跳转至匹配界面
            wx.navigateTo({
              url: '/pages/lism/lism',
            })
            app.globalData.userid=_this.data.userid
          }
        }
      }
    })
  }, 
  onLoad: function (options) {

  },

})