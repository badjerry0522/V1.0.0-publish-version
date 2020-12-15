//此页面是注册界面
const app=getApp();
const db = wx.cloud.database()
Page({
  onLoad:function(options){
    /*
    db.collection('num_user').doc("6127fe145fc654b600a65bb97bdb3b41").update({
      data:{
        tag:"number_user",
        number:0
      },
     success:function(res){
      console.log("reset complete")
     }
    })
    */
   //_id:6127fe145fc654b600a65bb97bdb3b41
   //_openid:o6l9J46jcKRzxEAUVDBe4Tk0wx_U
  },

  data:{
    array_sex:['male','female'],
    index_sex:0,
    array_constellation:['金牛','白羊','射手','双鱼','天秤','双子','魔蝎','天蝎','巨蟹','处女','水瓶','狮子'],
    index_constellation:0,
  },

  userinf:{
    name:"empty",
    wxid:"empty",
    phnum:"empty",
    gender:"male",
    constellation:'金牛',
    idea:""
  },
  userid:"empty",
  userpwd:"empty",
  NOU:-1,
 input_name: function (e) {
    this.userinf.name=e.detail.value//获取用户姓名
  },
  input_id:function(e){
    this.userid=e.detail.value;//获取用户的id
  },
  input_pwd:function(e){
    this.userpwd=e.detail.value;//获取用户密码
  },
  input_wxid: function (e) {
    this.userinf.wxid=e.detail.value//获取用户的微信id
  },

  input_phnum: function (e) {
    this.userinf.phnum=e.detail.value//获取用户手机号
  },

  input_idea:function(e){
    this.userinf.idea=e.detail.value//获取用户想对ta说的一句话
  },
  bindPickerChange_sex: function(e) {
    console.log('picker发送选择改变，携带值为', e.detail.value)
    this.setData({
      index_sex: e.detail.value
    })
    if(e.detail.value==0) this.userinf.gender='male';
    else this.userinf.gender='female';
    this.data.index_sex=e.detail.value
  },//用户选择自己的性别
 
  bindPickerChange_constellation: function(e) {
    console.log('picker发送选择改变，携带值为', e.detail.value)
    this.setData({
      index_constellation: e.detail.value
    })
    this.userinf.constellation=this.data.array_constellation[e.detail.value]
    this.data.index_constellation=e.detail.value
    console.log( this.userinf.constellation)
  },//用户选择自己的星座
  tap_submit:function(e){//提交用户信息
    if (!wx.cloud) {
      console.error('请使用 2.2.3 或以上的基础库以使用云能力')
    } else {
      wx.cloud.init({
        traceUser: true,
      })
    }
    var userid_temp=this.userid
    var _this=this
    console.log("userid_temp="),console.log(userid_temp)
    wx.cloud.callFunction({//查找要注册的用户id是否被注册过
      // 云函数名称
      name: 'search',
      // 传给云函数的参数
      data: {
        tag:userid_temp
      },
      success: function (res) {
        if(typeof(res.result.data[0])!="undefined"){//找到了该用户id，表明已注册过
          console.log("has established")
          console.log(res.result.data[0].dbuserinf)
        }
        else{//未找到用户id，表面未注册过
          db.collection('num_user').where({
          tag:"number_user"
          }).get({
            success:function(res){
              _this.NOU=res.data[0].number+1
              console.log(_this.NOU)
              db.collection('num_user').doc("6127fe145fc654b600a65bb97bdb3b41").update({//用户总数量+1
                  data:{
                    tag:"number_user",
                    number:res.data[0].number+1 
                  },
                  success:function(res){
                    console.log("set complete")
                  }
              })
              
              db.collection('1127').add({//在数据库中插入新用户的信息
                data:{
                  dbuserinf:_this.userinf,
                  userid:_this.userid,
                  userpwd:_this.userpwd,
                  tag:_this.userid,
                  userNO:_this.NOU,
                },
                success: function (res) {
                  console.log("NOU=")
                  console.log(_this.NOU)
                },
              })
            }
          })

          app.globalData.userid=_this.userid;
          wx.navigateTo({
            url: '/pages/lism/lism',//跳转至匹配界面
          })
        }
      },
      fail: console.error
    })

  }
  })