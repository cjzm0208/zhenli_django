var base_url='https://www.yzzhenli.org'




function upload_file (formdata) {
    if($('#file').val() === '') {
	          alert("Il faut choisir un dossier");
	     }else{
            $(".myprogress-hide").show();
            $.ajax({
                url: "/helper/uploadfile/",
                type: "post",
                contentType: false,
                processData: false,
                data: formdata,
                xhr: function () {
                    var xhr = new window.XMLHttpRequest();
                    xhr.upload.addEventListener("progress", function (evt) {
                        if (evt.lengthComputable) {
                            var percentComplete = evt.loaded / evt.total;
                            percentComplete = parseInt(percentComplete * 100);
                            console.log(percentComplete)
                            $('.myprogress').text(percentComplete + '%');
                            $('.myprogress').css('width', percentComplete + '%');
                            if (percentComplete == 100) {
                                $(".myprogress-hide").hide();
                                $(".file_upload").val("")
                            }
                        }
                    }, false);
                    return xhr;
                },
                success: function (data) {
                    console.log(data);
                    if(data="suc"){
                        dossier_type=$(".picker_img").attr("dossier_type")
                        show_image(0,dossier_type)
                    }else{
                        alert("Vous n'avez pas reussi d'uploader le document.")
                    }

                }
            });
        }
}

function show_image(n,dossier_type) {
    if(n==0){
        $(".picker_img").attr("page",0)
        $('#picker_img').html("")
    }
        $.ajax({
                url: "/helper/dossier/",
                type: "post",
                dataType:"json",
                data: {
                    'n':n,
                    'type':dossier_type
                },
                success: function (data) {
                    les_image=data
                    x=0
                    for (x in les_image){
                        if(les_image[x].type=='image'){
                        lien='<li orginal="'+les_image[x].lien+les_image[x].nom+'" num="'+les_image[x].id+'" nom="'+les_image[x].nom_org+'" type="'+les_image[x].type+'"><img src="'+les_image[x].lien+les_image[x].thumb+'"></li>'
                        }else if(les_image[x].type=='audio'){
                        lien='<li orginal="'+les_image[x].lien+les_image[x].nom+'" num="'+les_image[x].id+'" nom="'+les_image[x].nom_org+'" type="'+les_image[x].type+'" duration="'+parseInt(les_image[x].duration)+'"><img src="'+'/static/upload/commun/'+les_image[x].thumb+'"></li>'
                        }else if(les_image[x].type=='video'){
                        lien='<li orginal="'+les_image[x].lien+'" num="'+les_image[x].id+'" nom="'+les_image[x].nom_org+'" type="'+les_image[x].type+'"><img src="'+'/static/upload/commun/'+les_image[x].thumb+'"></li>'
                        }else{
                            lien='<li orginal="'+les_image[x].lien+les_image[x].nom+'" num="'+les_image[x].id+'" nom="'+les_image[x].nom_org+'" type="'+les_image[x].type+'"><img src="'+base_url+'static/upload/commun/'+les_image[x].thumb+'"></li>'
                        }
                        $('#picker_img').append(lien)
                    }
                    n_now=$(".picker_img").attr("page")
                    $(".picker_img").attr("page",parseInt(n_now)+1)
                    $(".picker_img").attr("dossier_type",dossier_type)
                    picker_img()
                }
            });
}

function picker_img(){
    $('.picker_img').children('li').click(function () {
        $(".picker_img").find(".picker_img_choisi").removeClass("picker_img_choisi");
        $(this).addClass('picker_img_choisi')
        type=$(this).attr("type")
        num=$(this).attr("num")
        $("#supprimer_dossier").attr('num',num)
        lien='<h6>'+$(this).attr("nom")+'</h6>'
        src=$(this).attr("orginal")
        if(type=='image'){
            lien+= '<img src="'+src+'">'
            $(".picker_img_prevoir").html(lien)
            window.parent.postMessage({
				 mceAction: 'customAction',
				 data: {
				    mon_message: '<img width="100%" src="' + src + '">'
				  }
			}, '*');

        }else if(type=='audio'){
            le_audio=lien+'<audio width="100%" id="player" src="'+src+'" type="audio/mp3" controls>'
            $(".picker_img_prevoir").html(le_audio)
            keyword="src="+src+"&type=audio"
            window.parent.postMessage({
				 mceAction: 'customAction',
				 data: {
				    mon_message: '<iframe class="tinymc_iframe" name="demo" src_org="'+src+'" le_type="audio" width="700" height="60" scrolling="no" frameborder="no" border="0"  src="/tinymc/iframe?'+keyword+'"></iframe>',
				  }
			}, '*');
            $('video,audio').mediaelementplayer();
        }else if(type=='video'){
            src=$(this).attr("orginal")
            le_video=lien+'<video id="prevoir_video" style="height:100%;"><source src="' + src + '" ></video>'
            $(".picker_img_prevoir").html(le_video)
			$('#prevoir_video').mediaelementplayer();
        }
        else {
            lien+= $(this).html()
            $(".picker_img_prevoir").html(lien)
        }
    })
}

$("#picker_img_box").scroll(function(){
     var allBoxHeight = $(".picker_img").height();
    var overflowBoxHeight = $("#picker_img_box").height();
    var scrollBoxHeight = $("#picker_img_box").scrollTop();
    if(overflowBoxHeight + scrollBoxHeight >allBoxHeight){
        n_now=parseInt($(".picker_img").attr("page"))
        dossier_type=$(".picker_img").attr("dossier_type")
        show_image(n_now,dossier_type)
        $(".picker_img").attr("page",n_now+1)
    }
})

function supprimer_dossier() {
    num=$(this).attr("num")
    console.log(num)
    // $("#picker_img").find('li[num="'+num+'"]').remove()
    $.ajax({
                url: "/helper/supprimer_dossier/",
                type: "post",
                dataType:"json",
                data: {
                    'id':num
                },
                success: function (data) {
                    console.log(data)
                    dossier_type=$(".picker_img").attr("dossier_type")
                    show_image(0,dossier_type)
                }
            });
}

function submit_ajouter_video() {
    var nom=$('#nom_video').val();
    var adresse=$('#adresse_video').val();
    $.ajax({
                url: "/helper/ajouter_video/",
                type: "post",
                dataType:"json",
                data: {
                    'nom_org':nom,
                    'lien':adresse,
                    'type':'video'
                },
                success: function (data) {
                    dossier_type=$(".picker_img").attr("dossier_type")
                    show_image(0,dossier_type)
                    $("#ajouter_video_input").hide()
                }
            });
}

$("#upload").click(function () {
         var formdata = new FormData();
         var csrf = $('input[name="csrfmiddlewaretoken"]').val();
         formdata.append("file", $("#file")[0].files[0]);
         formdata.append("csrfmiddlewaretoken",csrf);
        upload_file(formdata)
     });
 $("#but_picker_img").click(function () {
     var pour=$(this).attr('pour')
     src=$(".picker_img").find(".picker_img_choisi").attr('orginal');
     if(pour=="fichier_audio"){
         var duration=$(".picker_img").find(".picker_img_choisi").attr('duration');
         $("input[name='duration']").val(duration)
     $("input[name='fichier_audio']").val(src)
     var le_audio='<audio width="100%" id="player" src="'+src+'" type="audio/mp3" controls>'
         $("#audio_prevoir").html("")
         console.log(le_audio)
        $("#audio_prevoir").html(le_audio)
     }
     else if(pour=="fichier_video"){
         $("input[name='fichier_video']").val(src)
        le_video='<video style="height:100%;"><source src="' + src + '"  ></video>'
        $("#video_prevoir").html(le_video)
     }
     else if(pour=="visuel"){
         src=$(".picker_img").find(".picker_img_choisi").children('img').attr('src');
        $("input[name='visuel']").val(src)
         $("#img_visuel").attr('src',src)
     }
     else if(pour=="setting"){
         var name=$(this).attr('name')
        $("input[name='"+name+"']").val(src)
     }else if(pour=="new_content_audio"){
         var le_audio='<audio width="100%" id="player" src="'+base_url+src+'" type="audio/mp3" controls>'
        editoring.prev().html(le_audio)
         editoring.prev().attr("url",base_url+src)
         editoring.hide()
     }else if(pour=="new_content_video"){
         var le_video='<video style="height:100%;"><source src="' + src + '"  ></video>'
        editoring.prev().html(le_video)
         editoring.prev().attr("url",src)
         editoring.hide()
     }else if(pour=="new_content_image"){
         var le_image='<img width="100%"  src="'+src+'">'
        editoring.prev().html(le_image)
         editoring.prev().attr("url",src)
         editoring.hide()
     }
       $('video,audio').mediaelementplayer();
 })
 $("#id_fichier_video").change(function () {
     var src=$("input[name='fichier_video']").val()
     if(src) {
         var le_video = '<video style="height:100%;"><source src="' + src + '"  ></video>'
         $("#video_prevoir").html(le_video)
         $('video,audio').mediaelementplayer();
     }else {
         $("#video_prevoir").html('')
     }
 })
 $("#ajouter_video").click(function () {
     $("#ajouter_video_input").show()
 });
 $("#submit_ajouter_video").click(function () {
     submit_ajouter_video()
 });
 $("#supprimer_dossier").click(function () {
     supprimer_dossier()
     });


function fr_date(datetime) {
    if(datetime){
    if(datetime.indexOf(":")!=-1){
        datetime_arr=datetime.split(' ')
        date_arr=datetime_arr[0].split('-')
        return date_arr[2]+"-"+date_arr[1]+"-"+date_arr[0]+" "+datetime_arr[1]
    }else{
        date_arr=datetime.split('-')
        return date_arr[2]+"-"+date_arr[1]+"-"+date_arr[0]
    }
    }else{
        return ''
    }
}

function fr_que_date(datetime) {
    if(datetime.indexOf(":")!=-1){
        datetime_arr=datetime.split(' ')
        date_arr=datetime_arr[0].split('-')
        return date_arr[2]+"-"+date_arr[1]+"-"+date_arr[0]
    }else{
        date_arr=datetime.split('-')
        return date_arr[2]+"-"+date_arr[1]+"-"+date_arr[0]
    }
}

function colorRGBtoHex(color) {
    var rgb = color.split(',');
    var r = parseInt(rgb[0].split('(')[1]);
    var g = parseInt(rgb[1]);
    var b = parseInt(rgb[2].split(')')[0]);
    var hex = "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
    return hex;
 }
//parents
function add_parent(chambre,prenom,nom,relation,naissance) {
        parent_chambre=[]
        for(x in chambre){
            parent_chambre.push(chambre[x].numero)
        }
        un='<tr ><td id="chambre">'+parent_chambre.join(',')+'<textarea  style="display: none">'+JSON.stringify(chambre)+'</textarea></td><td id="prenom">'+prenom+'</td><td id="nom">'+nom+'</td><td id="relation">'+relation+'</td><td id="naissance">'+naissance+'</td><td><i class="fas fa-trash-alt parent_trash"></i></td></tr>'
        $("#parents_body").append(un)
        loads_parents()
}

function  loads_parents() {
    $(".parent_trash").click(function () {
        num=$(this).parent().parent().attr('num')
        if(num){
        }
         $(this).parent().parent().remove()
        that=$("#valide_parent")
        nombre=parseInt(that.attr('nombre'))
        that.attr('nombre',nombre-1)
        loads_parents()
    })

    tous_parents=[]
    $("#parents_body").children("tr").each(function () {
        un={}
        un['chambre']=JSON.parse($(this).children("#chambre").children("textarea").text())
        un['prenom']=$(this).children("#prenom").text()
        un['nom']=$(this).children("#nom").text()
        un['relation']=$(this).children("#relation").text()
        un['naissance']=$(this).children("#naissance").text()
        tous_parents.push(un)
    })
    nombre_parent=tous_parents.length
    $("input[name='Total']").val(nombre_parent+1)
    $("input[name='parent']").val(JSON.stringify(tous_parents))
}
//end parents

//inscription login
 $('#activide_login').click(function () {
        email=$('#activite_email').val()
        password=$('#activite_password').val()
        $.ajax({
                url: "/helper_cur/activite_login/",
                type: "post",
                dataType:"json",
                data: {
                    'email':email,
                    'password':password,
                },
                success: function (data) {
                    if(data=='exsit pas'){
                    $('#message').html('Email n\'est exsit pas')
                    }else if(data=='corresponds pas'){
                        $('#message').html('L\' email et le mots de passe ne sont pas corresponds')
                    }else {
                        location.reload()
                    }


                }
            });
    })

function addDate(date, days) {
		if (days == undefined || days == '') {
			days = 1;
		}
		var date = new Date(date);
		date.setDate(date.getDate() + days);
		var month = date.getMonth() + 1;
		var day = date.getDate();
		if(month<10){
			month='0'+''+month
		}
		if(day<10){
			day='0'+''+day
		}
		return date.getFullYear() + '-' + month + '-' + day;
	}


function daysBetween(sDate1,sDate2){
//Date.parse() 解析一个日期时间字dao符串，并返回1970/1/1 午夜距离该日期时间的毫秒数
var time1 = Date.parse(new Date(sDate1));
var time2 = Date.parse(new Date(sDate2));
var nDays = Math.abs(parseInt((time2 - time1)/1000/3600/24));
return nDays;
}

Date.prototype.Format = function (fmt) {
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "H+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}

$('#range_table_input').change(function () {
    l_val=$(this).val()
    fullWidth=$("#list").width()
    divWidth=$(".fixed-table-body").width()
    $(".fixed-table-body").scrollLeft(fullWidth*l_val/100);
})

function chapitre_list(value, row, index){
    var chapitres=JSON.parse(value)
    var res="<div style='width: 50rem;display: flex;flex-direction: row;flex-wrap: wrap'>"
    console.log(chapitres)
    $.each(chapitres,function (idx,val) {
        res+='<div style="width: 2rem" id="List_verse"><a href="/bible/chapitre/'+val+'/?book='+row.id+'">'+val+'</a></div>'
    })
    res+="</div>"
    return res
}

function fun_lecture_impair(value, row, index){
    var choices={1:"单数年",0:"双数年"}
    if(value || value==0){
        return choices[value]
    }else{
        return value
    }
}

function fun_lecture_abc(value, row, index){
    var choices={0:"A",1:"B",2:"C"}
    if(value || value==0){
        return choices[value]
    }else{
        return value
    }
}

function fun_lecture_abc(value, row, index){
    var choices={0:"A",1:"B",2:"C"}
    if(value || value==0){
        return choices[value]
    }else{
        return value
    }
}

function fun_lecture_fete(value, row, index){
    var choices={0:"纪",1:"节",2:"庆"}
    if(value || value==0){
        return choices[value]
    }else{
        return value
    }
}


function fun_prayer(value, row, index) {
     return  '<i class="fa fa-trash" id="delete_prayer" style="cursor: pointer" data-value="'+row.id+'"></i><i class="fa fa-times-circle ml-2" style="cursor: pointer" data-value="'+row.id+'" id="forbid_prayer"></i>'
}

$("body").on("click","#delete_prayer",function () {
    var id =$(this).attr("data-value")
    var token = $("input[name='csrfmiddlewaretoken']").val()
    var that=$(this)
    $.ajax({
                url: "/help/delete_prayer/",
                type: "post",
                dataType: "json",
                data: {
                    'id': id,
                    'csrfmiddlewaretoken': token,
                },
                success: function (data) {
                    that.parent().parent().remove()
                }
            });
})



$("body").on("click","#forbid_prayer",function () {
    var id =$(this).attr("data-value")
    var token = $("input[name='csrfmiddlewaretoken']").val()
    var that=$(this)
    $.ajax({
                url: "/help/forbid_prayer/",
                type: "post",
                dataType: "json",
                data: {
                    'id': id,
                    'csrfmiddlewaretoken': token,
                },
                success: function (data) {
                    alert("你已经屏蔽了此人。")
                    // that.parent().parent().remove()
                }
            });
})