


function bootstrap_table(data){
$('#list').bootstrapTable({
  //url:"/helper/inscription_pro/",
  columns:l_column,
  data:data,
  toolbar:"#toolbar",
  pagination: true,
  search: true,
  showColumns:true,
  //pageSize : 2,
    uniqueId:'id',
    pageList: [10, 25, 50, 100],
  detailView: true,
  showExport:true,
  // rowAttributes: function (row, index) {
  //      return {
  //          'insci_id': row.id,
  //      }
  // },
  onExpandRow: function(index, row, $detail) {
    var cur_table = $detail.html('<table></table>').find('table');
    var html = "";
    html += "<table class='table  table-striped table-bordered' style='margin-left: 2rem;width: auto'>";
    html += "<thead>";
    html += "<tr class='sub_table_title'>";
    html += "<th>Chambre</th>";
    html += "<th>Prénom</th>";
    html += "<th>Nom</th>";
    html += "<th>Relation</th>";
    html += "<th>Naissance</th>";
    html += "</tr>";
    html += "</thead>";
    if(row.parent){
    parents=JSON.parse(row.parent)
    html += "<tbody>";
            for(y in parents){
                html += "<tr>";
                if(row.date_arrive && row.date_depart){
                  date_arrive=row.date_arrive
                  date_depart=row.date_depart
                  if(date_depart>date_arrive){
                      if(parents[y].chambre){
                      chambres=parents[y].chambre
                      les_chambre=""
                      if(chambres.length>0){
                      for (x in chambres){
                          les_chambre+='<button type="button" index="'+y+'" row_index="'+index+'" num="'+row.id+'" class="btn btn-block btn-success btn-sm choisir_le_chambre"><fa class="'+chambres[x].lit_matela+'"></fa>'+chambres[x].numero+'</button>'
                      }
                      }else{
                          les_chambre= '<button type="button" index="'+y+'" row_index="'+index+'" num="'+row.id+'" class="btn btn-block btn-success btn-sm choisir_le_chambre">Chambre</button>'
                      }
                      }else{
                          les_chambre= '<button type="button" index="'+y+'" row_index="'+index+'" num="'+row.id+'" class="btn btn-block btn-success btn-sm choisir_le_chambre">Chambre</button>'
                      }
                  }else{
                      les_chambre= '<button type="button" index="'+y+'" class="btn btn-block btn-secondary btn-sm">Chambres</button>'
                  }
              }
                html += "<td>"+les_chambre+"</td>";
                html += "<td>"+parents[y].prenom+"</td>";
                html += "<td>"+parents[y].nom+"</td>";
                html += "<td>"+parents[y].relation+"</td>";
                html += "<td>"+naissance(fr_date(parents[y].naissance),row)+"</td>";
                html += "</tr>";
            }
            html += "</tbody>";
            html += '</table>';
            $detail.html(html);
        }
},
onLoadSuccess:function(data){
},
  formatLoadingMessage: function () {  //加载成功时执行
    },
})
}
//$('#list').on('all.bs.table', function (e, name, args) {
//    console.log('load-success');
//})
window.choisir_chambre = {
    'click .choisir_le_chambre': function (e, value, row, index) {
        show_chambres(row.chambre,row.id,-1,row.date_arrive,row.date_depart,index)
 }
};
var globel_date_arrive=''
var globel_date_depar=''

function show_chambres(les_chambres,id,parent,date_arrive,date_depart,index){
            $('#chambre').modal('show')
            globel_date_depar=date_depart
            globel_date_arrive=date_arrive
            $('#lieus').children().first().children('.nav-link').addClass('active')
            lieu='Toutes'
            $("#enreg_chambres").attr("inscri_id",id)
            $("#enreg_chambres").attr("parent",parent)
            $("#enreg_chambres").attr("index",index)
             $('#chambres_choisi').html("")
            if(les_chambres){
                chambres=JSON.parse(les_chambres)
                for(x in chambres){
                    un_chambre='<span class="btn btn-primary btn-sm is_choisi_list" lieu="'+chambres[x].lieu+'" numero="'+chambres[x].numero+'" lit_matela="'+chambres[x].lit_matela+'"><span>'+chambres[x].lieu+'</span><fa class="'+chambres[x].lit_matela+'"></fa>'+chambres[x].numero+'</span>'
            $('#chambres_choisi').append(un_chambre)
                }
            }
            lieu_chambre(lieu,function () {
                chambre_coupe(date_arrive,date_depart,lieu)
            })

}

$(".lieu_list").click(function () {
    lieu=$(this).text()
    g_lieu=lieu
    lieu_chambre(lieu,function () {
        chambre_coupe(globel_date_arrive,globel_date_depar,lieu)
    })
})
function lieu_chambre(lieu,callback){
    $("#chambres_list").html("")
    chambres_choisi=[]
    $("#chambres_choisi").children().each(function () {
        un_lieu=$(this).attr("lieu")
        un_numero=$(this).attr("numero")
        un_lit_matela=$(this).attr("lit_matela")
        un={'lieu':un_lieu,'numero':un_numero,'lit_matela':un_lit_matela}
        chambres_choisi.push(un)
    })
    for(x in g_chambres){
        i=0
        lit_choisi=""
        matela_choisi=""
        berceau_choisi=""
        autre_choisi=""
        for(i in chambres_choisi){
            if(g_chambres[x].numero==chambres_choisi[i].numero && chambres_choisi[i].lieu==lieu){
                if(chambres_choisi[i].lit_matela=="fas fa-bed"){
                    lit_choisi='is_choisi'
                }else  if(chambres_choisi[i].lit_matela=="fas fa-window-minimize"){
                    matela_choisi='is_choisi'
                }else  if(chambres_choisi[i].lit_matela=="fas fa-child"){
                    berceau_choisi='is_choisi'
                }else  if(chambres_choisi[i].lit_matela=="fas fa-eraser"){
                    autre_choisi='is_choisi'
                }
            }
        }
        if(lieu!='Toutes'){
            if(g_chambres[x].lieu==lieu){
        un='<div class="card col-md-2">\n' +
            '              <div class="card-header p-0 ">\n' +
            g_chambres[x].numero  +
            '              </div><!-- /.card-header -->\n' +
            '              <div class="row">\n' +
            '                  <div class="col-md-6 un_chambre" numero="'+g_chambres[x].numero +'">\n' +
            '                      <span class="btn btn-primary btn-sm col-md-12 choisir_chambre '+lit_choisi+'" signe="'+g_chambres[x].lieu+'-'+g_chambres[x].numero+'-fas fa-bed'+'"><fa class="fas fa-bed"></fa><span id=occupe>0</span>/<span id="avoir">'+g_chambres[x].lit+'</span></span>\n' +
            '                      <span class="btn btn-primary btn-sm col-md-12 choisir_chambre '+matela_choisi+'" signe="'+g_chambres[x].lieu+'-'+g_chambres[x].numero+'-fas fa-window-minimize'+'"><fa class="fas fa-window-minimize"></fa><span id=occupe>0</span>/<span id="avoir">'+g_chambres[x].matela+'</span></span>\n' +
            '                      <span class="btn btn-primary btn-sm col-md-12 choisir_chambre '+berceau_choisi+'" signe="'+g_chambres[x].lieu+'-'+g_chambres[x].numero+'-fas fa-child'+'"><fa class="fas fa-child"></fa></fa><span id=occupe>0</span>/<span id="avoir">'+g_chambres[x].berceau+'</span></span>\n' +
            '                      <span class="btn btn-primary btn-sm col-md-12 choisir_chambre '+autre_choisi+'" signe="'+g_chambres[x].lieu+'-'+g_chambres[x].numero+'-fas fa-eraser'+'"><fa class="fas fa-eraser"></fa><span id=occupe>0</span>/<span id="avoir">'+g_chambres[x].autre+'</span></span>\n' +
            '                  </div>\n' +
                '<div class="col-md-6 le-detail"></div>'+
            '                </div>\n' +
            '                <!-- /.tab-content -->\n' +
            '            </div>'
            $("#chambres_list").append(un)
                }
        }else{
            un=''
            if(x>0 && g_chambres[x].lieu!=g_chambres[x-1].lieu){
                un='<div class=" col-md-12"><strong>'+g_chambres[x].lieu+'</strong></div>'
            }else if(x==0){
                un='<div class=" col-md-12"><strong>'+g_chambres[x].lieu+'</strong></div>'
            }
             un+='<div class="card col-md-1">\n' +
            '              <div class="card-header p-0 ">\n' +
            g_chambres[x].numero  +
            '              </div><!-- /.card-header -->\n' +
            '              <div class="row">\n' +
            '                  <div class="col un_chambre" numero="'+g_chambres[x].numero +'">\n' +
            '                      <span class="btn btn-primary btn-sm col-md-12 '+lit_choisi+'" signe="'+g_chambres[x].lieu+'-'+g_chambres[x].numero+'-fas fa-bed'+'"><fa class="fas fa-bed"></fa><span id=occupe>0</span>/<span id="avoir">'+g_chambres[x].lit+'</span></span>\n' +
            '                  </div>\n' +
            '            </div>'+
            '            </div>'
            $("#chambres_list").append(un)
        }

    }
    callback()
}

function chambre_coupe(date_arrive,date_depart,lieu) {
    les_chambres=[]
    day=date_arrive
    days=[]
    un=[]
    while (day<=date_depart){
        if(date_arrive==day){
            un=[date_arrive,day+' 23:59:59']
        }else if(date_depart.indexOf(day)!= -1){
            un=[day+' 00:00:00',date_depart]
        }else{
            un=[day+' 00:00:00',day+' 23:59:59']
        }
        days.push(un)
        day=addDate(day,1)
    }

    for(x in data){
        if(data[x].date_depart && data[x].date_arrive) {
            if (dans_tot_tard(date_arrive,date_depart,data[x].date_arrive,data[x].date_depart)) {
                les_chambres_inscri = JSON.parse(data[x].chambre)
                for (l1 in les_chambres_inscri) {
                    les_chambres_inscri[l1].id = data[x].id
                    les_chambres_inscri[l1].prenom = data[x].prenom
                    les_chambres_inscri[l1].nom = data[x].nom
                    les_chambres_inscri[l1].sex = data[x].sex
                    les_chambres_inscri[l1].titre = data[x].activite_titre
                    les_chambres_inscri[l1].date_arrive=data[x].date_arrive
                    les_chambres_inscri[l1].date_depart=data[x].date_depart
                    les_chambres.push(les_chambres_inscri[l1])
                }
            if(data[x].parent){
                les_parent = JSON.parse(data[x].parent)
                for (i in les_parent) {
                    un_chambre = les_parent[i].chambre
                    for (l2 in un_chambre) {
                        un_chambre[l2].id = data[x].id
                        un_chambre[l2].sex = les_parent[i].relation
                        un_chambre[l2].titre = data[x].activite_titre
                        un_chambre[l2].prenom = les_parent[i].prenom
                        un_chambre[l2].nom = les_parent[i].nom
                        un_chambre[l2].date_arrive=data[x].date_arrive
                        un_chambre[l2].date_depart=data[x].date_depart
                        les_chambres.push(un_chambre[l2])
                    }
                }
            }
            }
        }
    }
    new_chambres=[]
    for(n in les_chambres){
        un_ch={numero:les_chambres[n].numero,lieu:les_chambres[n].lieu,lit_matela:les_chambres[n].lit_matela}
        if(JSON.stringify(new_chambres).indexOf(JSON.stringify(un_ch))<0){
            new_chambres.push(un_ch)
        }
    }
    meme_chambre=[]
    for(u in new_chambres){
        un_meme_chambre=[]
        for(n in les_chambres){
            if(new_chambres[u].numero==les_chambres[n].numero && new_chambres[u].lieu==les_chambres[n].lieu && new_chambres[u].lit_matela==les_chambres[n].lit_matela){
                un_meme_chambre.push(les_chambres[n])
            }
        }
        meme_chambre.push({chambre:new_chambres[u],inscris:un_meme_chambre})
    }
    for(j in meme_chambre){
        if(meme_chambre[j].inscris.length>1){
            personnes=meme_chambres(meme_chambre[j].inscris)
            that1=$("#chambres_list").find("span[signe='"+personnes[0].lieu+'-'+personnes[0].numero+'-'+personnes[0].lit_matela+"']")
            avoir=that1.children("#avoir").text()
            occupe=personnes.length
            that1.children("#occupe").text(occupe)
            if(occupe == parseInt(avoir)){
                that1.css("background",'#6610f2')
            }else if(occupe<parseInt(avoir)){
                that1.css("background",'#23923d')
            }else{
                that1.css("background",'#ffc107')
            }
            le_detail=that1.parent().next()
            for(h in personnes){
                un='<div class="un_detail" title="'+personnes[h].titre+'" data-placement="right"><p>'+personnes[h].titre+'</p><p>'+personnes[h].prenom+'</p><p>'+personnes[h].nom+'</p><p>'+personnes[h].sex+'</p></div>'
                le_detail.append(un)
            }
        }else{
            console.log(meme_chambre[j])
            that1=$("#chambres_list").find("span[signe='"+meme_chambre[j].chambre.lieu+'-'+meme_chambre[j].chambre.numero+'-'+meme_chambre[j].chambre.lit_matela+"']")
            avoir=that1.children("#avoir").text()
            occupe=1
            that1.children("#occupe").text(occupe)
            if(occupe == parseInt(avoir)){
                that1.css("background",'#6610f2')
            }else if(occupe<parseInt(avoir)){
                that1.css("background",'#23923d')
            }else{
                that1.css("background",'#ffc107')
            }
            le_detail=that1.parent().next()
            un='<div class="un_detail" title="'+meme_chambre[j].inscris[0].titre+'" data-placement="right"><p>'+meme_chambre[j].inscris[0].titre+'</p><p>'+meme_chambre[j].inscris[0].prenom+'</p><p>'+meme_chambre[j].inscris[0].nom+'</p><p>'+meme_chambre[j].inscris[0].sex+'</p></div>'
            le_detail.append(un)
        }
    }
    // for(z in new_chambres){
    //     com=combien_personnes(new_chambres[z],days,les_chambres)
    //     if(com){
    //         that1=$("#chambres_list").find("span[signe='"+com[0].lieu+'-'+com[0].numero+'-'+com[0].lit_matela+"']")
    //         avoir=that1.children("#avoir").text()
    //         occupe=com.length
    //         that1.children("#occupe").text(occupe)
    //         if(occupe==parseInt(avoir)){
    //             that1.css("background",'#6610f2')
    //         }else if(occupe<parseInt(avoir)){
    //             that1.css("background",'#23923d')
    //         }else{
    //             that1.css("background",'#ffc107')
    //         }
    //         le_detail=that1.parent().next()
    //         for(h in com){
    //             un='<div class="un_detail" title="'+com[h].titre+'" data-placement="right"><p>'+com[h].titre+'</p><p>'+com[h].prenom+'</p><p>'+com[h].nom+'</p><p>'+com[h].sex+'</p></div>'
    //             le_detail.append(un)
    //         }
    //     }
    // }
    // for(m in les_chambres){
    //         that1=$("#chambres_list").find("span[signe='"+les_chambres[m].lieu+'-'+les_chambres[m].numero+'-'+les_chambres[m].lit_matela+"']")
    //         occupe=that1.children("#occupe").text()
    //         avoir=that1.children("#avoir").text()
    //         occupe=parseInt(occupe)+1
    //         that1.children("#occupe").text(occupe)
    //         if(occupe==parseInt(avoir)){
    //             that1.css("background",'#6610f2')
    //         }else if(occupe<parseInt(avoir)){
    //             that1.css("background",'#23923d')
    //         }else{
    //             that1.css("background",'#ffc107')
    //         }
    //     le_detail=that1.parent().next()
    //         un='<div class="un_detail" title="'+les_chambres[m].titre+'" data-placement="right"><p>'+les_chambres[m].titre+'</p><p>'+les_chambres[m].prenom+' '+les_chambres[m].nom+'</p><p>'+les_chambres[m].sex+'</p></div>'
    //         le_detail.append(un)
    // }
    tip()
}

function meme_chambres(inscris) {
    new_inscris=[]
    sans_meler=[inscris[0]]
    dif={}
    for(x in inscris){
        si_meme=false
        for(y in sans_meler){
            if(dans_tot_tard(inscris[x].date_arrive,inscris[x].date_depart,sans_meler[y].date_arrive,sans_meler[y].date_depart)){
                si_meme=si_meme|true
            }else{
                si_meme=si_meme|false
            }
        }
        if(!si_meme){
            sans_meler.push(inscris[x])
        }
    }
    for(x1 in inscris){
        si_meme=false
        for(y1 in sans_meler){
            if(dans_tot_tard(inscris[x1].date_arrive,inscris[x1].date_depart,sans_meler[y1].date_arrive,sans_meler[y1].date_depart)){
                if(!dif[y1]){
                    dif[y1]=[]
                }
                dif[y1].push(inscris[x1])
            }
        }
    }
    mmm=0
    max_personne=[]
    $.each(dif, function(i, val) {
        if(val.length>mmm){
            mmm=val.length
            max_personne=val
        }
    });
    return max_personne
}

function combien_personnes(chambre,jour,inscris){
    l2=0
    qui2=[]
    for(un in jour){
        ll=0
        qui=[]
    for(y in inscris){
        if(inscris[y].numero==chambre.numero && inscris[y].lieu==chambre.lieu && inscris[y].lit_matela==chambre.lit_matela){
                l_in=dans_tot_tard(inscris[y].date_arrive,inscris[y].date_depart,jour[un][0],jour[un][1])
                if(l_in){
                    qui.push(inscris[y])
                    ll++
                }
            }
        }
    if(ll>l2){
        l2=ll
        qui2=qui
    }
    }
    // if(qui2.length>1){
    //     if(qui2[0].date_arrive<qui2[1].date_arrive){
    //         if(qui2[0].date_depart<qui2[1].date_arrive){
    //             return [qui2[0]]
    //         }else{
    //             return qui2
    //         }
    //     }else{
    //         if(qui2[1].date_depart<qui2[0].date_arrive){
    //             return [qui2[0]]
    //         }else{
    //             return qui2
    //         }
    //     }
    // }else{
        return qui2
    // }
}
function dans_tot_tard(date_arrive,date_depart,x_date_arrive,x_date_depart) {
    if(x_date_arrive >= date_arrive && x_date_depart <= date_depart){
                dans=true
            }else{
                dans=false
            }
            if(x_date_arrive <= date_arrive && x_date_depart >= date_arrive){
                tot=true
            }else{
                tot=false
            }
            if(x_date_arrive <= date_depart && x_date_depart >= date_depart){
                tard=true
            }else{
                tard=false
            }
            return dans|tot|tard
}

function tip() {
    $("[data-toggle='tooltip']").tooltip();
}
    $('body').on('click','.choisir_chambre',function () {
        numero=$(this).parent().attr('numero')
        that=$(this).children().first().clone()
        lit_matela=that.attr("class")
        //if($(this).hasClass('is_choisi')){
        //    $(this).removeClass('is_choisi')
        //    $("#chambres_choisi").children("span[lieu='"+lieu+"'][numero='"+numero+"'][lit_matela='"+lit_matela+"']").remove()
        //}else {
            $(this).addClass('is_choisi')
            un_chambre='<span class="btn btn-primary btn-sm is_choisi_list" lieu="'+g_lieu+'" numero="'+numero+'" lit_matela="'+lit_matela+'"><span>'+g_lieu+'</span>'+that.prop("outerHTML")+numero+'</span>'
            $('#chambres_choisi').append(un_chambre)
        //}
    })

    $('body').on('click','.is_choisi_list',function () {
        numero=$(this).attr("numero")
        lit_matela=$(this).attr("lit_matela")
        lieu_chamb=$(this).attr("lieu")
        if(lieu_chamb==g_lieu){
            $("#chambres_list").find("div[numero='"+numero+"']").find("fa[class='"+lit_matela+"']").parent().removeClass("is_choisi")
        }
        $(this).remove()
    })


$("#enreg_chambres").click(function () {
    l_id=$(this).attr("inscri_id")
    l_parent=$(this).attr("parent")
    chambres_choisi=[]
        $("#chambres_choisi").children().each(function () {
            un_lieu=$(this).attr("lieu")
            un_numero=$(this).attr("numero")
            un_lit_matela=$(this).attr("lit_matela")
            un={'lieu':un_lieu,'numero':un_numero,'lit_matela':un_lit_matela}
            chambres_choisi.push(un)
        })
        if(l_parent<0){
            $.ajax({
                url: "/helper/save_chambres/",
                type: "post",
                dataType:"json",
                async:false,
                data: {
                    'id':l_id,
                    'chambres':JSON.stringify(chambres_choisi),
                },
                success: function (data_row) {
                $('#list').bootstrapTable('updateCellByUniqueId', {id: l_id,field: 'chambre',value: JSON.stringify(chambres_choisi)});
                }
            });
        }else{
            for(x in data){
                  if(data[x].id==parseInt(l_id)){
                      un_parent=data[x]
                      parent_chambres=JSON.parse(un_parent.parent)
                      parent_chambres[index].chambre=chambres_choisi
                      $.ajax({
                            url: "/helper/save_parent_chambres/",
                            type: "post",
                            dataType:"json",
                            data: {
                                'id':l_id,
                                'parents':JSON.stringify(parent_chambres),
                            },
                            success: function (data_row) {
                                 $('#list').bootstrapTable('updateCellByUniqueId', {id: l_id,field: 'parent',value: JSON.stringify(parent_chambres)});
                                 $(".detail-icon").each(function () {
                                    $(this).trigger("click")
                                })
                            }
                        });
                      break
                  }
              }

        }
})




  $('#list').on( 'page-change.bs.table', function ( e, number, size ) {
      pre_page=number
  })
$('body').on('click','.choisir_le_chambre',function () {
    num=$(this).attr("num")
      index=$(this).attr("index")
      row_index=$(this).attr("row_index")
      for(x in data){
          if(data[x].id==parseInt(num)){
              un_parent=data[x]
              parent_chambres=JSON.parse(un_parent.parent)
              show_chambres(JSON.stringify(parent_chambres[index].chambre),num,index,un_parent.date_arrive,un_parent.date_depart,row_index)
              break
          }
      }
})


$("#deplier").click(function () {
    if($(this).text()=="Déplier"){
        $(this).text('Plier')
    }else{
        $(this).text('Déplier')
    }
    $(".detail-icon").each(function () {
        $(this).trigger("click")
    })
})

function prenom(value, row, index) {
   if(row.formule==null){
       return '<a href="/inscription/edit_form/'+row.id+'" target="_blank">'+value+'</a>'
   }else{
       return '<a href="/formule/formule_edit/'+row.id+'" target="_blank">'+value+'</a>'}
}
  function chambre (value, row, index) {
          value=row.chambre
          les_chambre=""
      if(row.date_arrive && row.date_depart){
          date_arrive=row.date_arrive
          date_depart=row.date_depart
          if(date_depart>date_arrive){
              if(value){
              chambres=JSON.parse(value)
              if(chambres.length>0) {
                  les_chambre+='<div class="tr-chambre">'
                  for (x in chambres) {
                      les_chambre += '<button type="button" class="btn btn-block btn-success btn-sm choisir_le_chambre"><fa class="' + chambres[x].lit_matela + '"></fa>' + chambres[x].numero + '</button>'
                  }
                  les_chambre+='</div>'
              }else{
                   les_chambre= '<button type="button" class="btn btn-block btn-success btn-sm choisir_le_chambre">Chambre</button>'
              }
              }else{
                  les_chambre= '<button type="button" class="btn btn-block btn-success btn-sm choisir_le_chambre">Chambre</button>'
              }
          }else{
              les_chambre= '<button type="button" class="btn btn-block btn-secondary btn-sm">Chambres</button>'
          }
      }else{
          les_chambre= '<button type="button" class="btn btn-block btn-secondary btn-sm">Chambres</button>'
      }
      return les_chambre
      choisir()
  }

  function email_confirmer(value, row, index) {
        if(value){
            return '<a class="nav-link">\n' +
            '          <i class="fas fa-envelope text-warning" id="email_confirmer" num="'+row.id+'" style="font-size: 2rem; cursor: pointer"></i>\n' +
            '          <span class="badge badge-danger">'+value+'</span>\n' +
            '        </a>'
        }else{
           return '<a class="nav-link">\n' +
            '          <i class="fas fa-envelope text-warning" id="email_confirmer" num="'+row.id+'"  style="font-size: 2rem; cursor: pointer"></i>\n' +
            '          <span class="badge badge-danger">'+0+'</span>\n' +
            '        </a>'
        }
  }

  function confirmer_reponse(value, row, index) {
        if(value){
            return '<i class="fas fa-check-circle text-success" style="font-size: 2rem;"></i>'
        }else{
            return '<i class="fas fa-times-circle" style="font-size: 2rem;"></i>'
        }
  }

  function venue_imminente(value, row, index) {
        if(value){
            return '<a class="nav-link">\n' +
            '          <i class="fas fa-envelope text-warning" id="email_retraitent" type="venue_imminente" num="'+row.id+'" style="font-size: 2rem; cursor: pointer"></i>\n' +
            '          <span class="badge badge-danger">'+value+'</span>\n' +
            '        </a>'
        }else{
           return '<a class="nav-link">\n' +
            '          <i class="fas fa-envelope text-warning" id="email_retraitent" type="venue_imminente" num="'+row.id+'"  style="font-size: 2rem; cursor: pointer"></i>\n' +
            '          <span class="badge badge-danger">'+0+'</span>\n' +
            '        </a>'
        }
  }

  function venue_imminente_reponse(value, row, index) {
        if(value){
            return '<i class="fas fa-check-circle text-success" id="venue_imminente_reponse" val=0 index="'+index+'"  num="'+row.id+'" style="font-size: 2rem;cursor: pointer"></i>'
        }else{
            return '<i class="fas fa-times-circle" id="venue_imminente_reponse" val=1 index="'+index+'" num="'+row.id+'" style="font-size: 2rem;cursor: pointer"></i>'
        }
  }
    $('body').on('click','#venue_imminente_reponse',function () {
        l_val= $(this).attr("val")
        l_index= $(this).attr("index")
        num= $(this).attr("num")
        $.ajax({
            url: "/helper/venue_imminente_reponse/",
            type: "post",
            dataType:"json",
            data: {
                num:num,
                val:l_val,
            },
            success: function (res) {
                if(res){
                    $('#list').bootstrapTable('updateCellByUniqueId', {id: num,field: 'venue_imminente_reponse',value:parseInt(l_val)});
                }
            }
        });
    })

function payee(value, row, index) {
        if(value=="Oui"){
            return '<i class="fas fa-check-circle text-success" id="payee" val="Non" index="'+index+'"  num="'+row.id+'" style="font-size: 2rem;cursor: pointer"></i>'
        }else{
            return '<i class="fas fa-times-circle" id="payee" val="Oui" index="'+index+'" num="'+row.id+'" style="font-size: 2rem;cursor: pointer"></i>'
        }
  }

  $('body').on('click','#payee',function () {
        l_val= $(this).attr("val")
        l_index= $(this).attr("index")
        num= $(this).attr("num")
        $.ajax({
            url: "/helper/payee/",
            type: "post",
            dataType:"json",
            data: {
                num:num,
                val:l_val,
            },
            success: function (res) {
                if(res){
                    $('#list').bootstrapTable('updateCellByUniqueId', {id: num,field: 'payee',value:l_val});
                }
            }
        });
    })
function payee1(value, row, index) {
        if(value=="Oui"){
            return '<i class="fas fa-check-circle text-success" id="payee1" val="Non" index="'+index+'"  num="'+row.id+'" style="font-size: 2rem;cursor: pointer"></i>'
        }else{
            return '<i class="fas fa-times-circle" id="payee1" val="Oui" index="'+index+'" num="'+row.id+'" style="font-size: 2rem;cursor: pointer"></i>'
        }
  }
  $('body').on('click','#payee1',function () {
        l_val= $(this).attr("val")
        l_index= $(this).attr("index")
        num= $(this).attr("num")
        $.ajax({
            url: "/helper/payee1/",
            type: "post",
            dataType:"json",
            data: {
                num:num,
                val:l_val,
            },
            success: function (res) {
                if(res){
                    $('#list').bootstrapTable('updateCellByUniqueId', {id: num,field: 'payee1',value:l_val});
                }
            }
        });
    })

  function parent(value, row, index) {
    if(value){
        values=JSON.parse(value)
        new_parents=[]
        for(x_pa in values){
            new_parents.push(values[x_pa].prenom+'/'+values[x_pa].naissance+'/'+values[x_pa].relation)
        }
        return new_parents.join(",")
        }else {
        return ''
    }
  }

  function repas(value, row, index) {
    if(row.repas){
      values=JSON.parse(value)
    date_arrive=row.date_arrive
    date_depart=row.date_depart
    if(date_arrive && date_depart){
        date_arrive_arr=date_arrive.split(" ")
        date_arrive=date_arrive_arr[0]
        date_depart_arr=date_depart.split(" ")
        date_depart=date_depart_arr[0]
        if(date_depart >= date_arrive){
            day=date_arrive
            l_html='<div class="tr-chambre" style="text-align: center"><table class="table table-bordered"><thead>\n' +
                '<tr><th>Petit déjeuner</th><th>Déjeuner</th><th>Dîner</th></tr></thead><tbody id="repas_body">'
            while (day <= date_depart){
                checked_pdj=''
                 checked_dej=''
                checked_din=''
                if($.inArray('pdej'+day, values) > -1){
                    checked_pdj='text-success'
                }
                if($.inArray('dej'+day, values) > -1){
                    checked_dej='text-success'
                }
                if($.inArray('din'+day, values)  > -1){
                    checked_din='text-success'
                }
                l_html+='<tr><td class="'+checked_pdj+'">'+day+'</td>' +
                '<td class="'+checked_dej+'">'+day+'</td>' +
                '<td class="'+checked_din+'">'+day+'</td></tr>'
                day=addDate(day,1)
            }
            l_html+='</tbody></table></div>'
        }
    }

    }else{
        l_html=''
    }
        return l_html
  }
  function fun_date_arrive(value, row, index) {
    if(value) {
        if (value.indexOf(":") != -1) {
            datetime_arr = value.split(' ')
            date_arr = datetime_arr[0].split('-')
            return '<div class="fun_date_arrive text-primary" style="cursor: pointer" num="'+row.id+'">' +date_arr[2] + "-" + date_arr[1] + "-" + date_arr[0] + " " + datetime_arr[1]+'</div>'
        } else {
            date_arr = value.split('-')
            return '<div class="fun_date_arrive text-primary" style="cursor: pointer" num="'+row.id+'">' +date_arr[2] + "-" + date_arr[1] + "-" + date_arr[0]+'</div>'
        }
    }
  }
  function fun_date_depart(value, row, index) {
    if(value) {
        if (value.indexOf(":") != -1) {
            datetime_arr = value.split(' ')
            date_arr = datetime_arr[0].split('-')
            return '<div class="fun_date_depart text-primary" style="cursor: pointer" num="'+row.id+'">' +date_arr[2] + "-" + date_arr[1] + "-" + date_arr[0] + " " + datetime_arr[1]+'</div>'
        } else {
            date_arr = value.split('-')
            return '<div class="fun_date_depart text-primary" style="cursor: pointer" num="'+row.id+'">' +date_arr[2] + "-" + date_arr[1] + "-" + date_arr[0]+'</div>'
        }
    }
  }
  $('body').on('click','.fun_date_arrive,.fun_date_depart',function () {
      if($(this).attr('class')=='fun_date_arrive text-primary'){
          l_type='date_arrive'
      }else{
          l_type='date_depart'
      }
      $(this).parent().html('<div class="input-group mb-3 justify-content-end" style="">\n' +
        '                  <input type="text" class="form-control-sm datetime_input" value="'+$(this).text()+'">\n' +
        '                  <div class="btn btn-sm btn-primary submit_date" style="width:50%;margin-top: 0.5rem" num="'+$(this).attr('num')+'" type="'+l_type+'">\n' +
        '                   <i class="fas fa-check"></i>\n' +
        '                  </div>\n' +
        '                </div>')
      var fp_time = flatpickr(".datetime_input", {
		enableTime: true,
		dateFormat: "d-m-Y H:i:S",
		time_24hr:true,
		locale: "fr"  // locale for this instance only
	})
  })


  $("body").on('click','.submit_date',function () {
      l_val=fr_date($(this).parent().children('input').val())
      num=$(this).attr('num')
      l_champ=$(this).attr('type')
      console.log(l_val)
      upload_value(num,l_champ,l_val)
  })
function retour_argent(value,row,index) {
    if(value){
        return '<button class="btn-sm btn-default" disabled>Retour</button>'
    }else{
        if(row.date_payee){
            now = new Date();
            console.log(row.date_payee)
            daysdif=daysBetween(row.date_payee,now.Format("yyyy-MM-dd HH:mm:ss"))
            if(daysdif<3 && row.payee=='Oui' && row.somme>0){
                return '<a href="/inscription_pro/retour_argent/'+row.id+'/?type=inscription" class="btn-sm btn-primary" target="_blank">Retour</a>'
            }else{
                return '<button class="btn-sm btn-default" disabled>Retour</button>'
            }
        }else{
            return '<button class="btn-sm btn-default" disabled>Retour</button>'
        }
    }
}
function retour_argent1(value,row,index) {
    if(value){
        return '<button class="btn-sm btn-default" disabled>Retour</button>'
    }else{
        if(row.date_payee){
            now = new Date();
            daysdif=daysBetween(row.date_payee1,now.Format("yyyy-MM-dd HH:mm:ss"))
            if(daysdif<3 && row.payee1=='Oui' && row.somme1>0){
                return '<a href="/inscription_pro/retour_argent/'+row.id+'/?type=acitivte" class="btn-sm btn-primary" target="_blank">Retour</a>'
            }else{
                return '<button class="btn-sm btn-default" disabled>Retour</button>'
            }
        }else{
            return '<button class="btn-sm btn-default" disabled>Retour</button>'
        }
    }
}
//上传值函数
function upload_value(id,champ,vaule) {
    $.ajax({
            url: "/helper/upload_value/",
            type: "post",
            dataType:"json",
            data: {
                id:id,
                val:vaule,
                champ:champ
            },
            success: function (res) {
                if(res){
                    $('#list').bootstrapTable('updateCellByUniqueId', {id: id,field: champ,value:vaule});
                }
            }
        });
}
  function arrive(value, row, index) {
        if(value){
           res='<i class="fas fa-check-circle text-success" index="'+index+'" type="arrive" num="'+row.id+'" id="click_arrive_partir" val=0  style="font-size: 2rem; cursor: pointer"></i>'
        }else{
          res='<i class="fas fa-times-circle" index="'+index+'" id="click_arrive_partir" num="'+row.id+'" val=1 type="arrive" style="font-size: 2rem;cursor: pointer"></i>'
        }
        return res
  }

  function partir(value, row, index) {
        if(value){
           res='<i class="fas fa-check-circle text-success" index="'+index+'" num="'+row.id+'" type="partir" id="click_arrive_partir" val=0 style="font-size: 2rem;cursor: pointer"></i>'
        }else{
          res='<i class="fas fa-times-circle " index="'+index+'" val=1 type="partir" num="'+row.id+'" id="click_arrive_partir" style="font-size: 2rem;cursor: pointer"></i>'
        }
        return res
  }


$("body").on("click",'#email_retraitent',function () {
    num=$(this).attr("num")
    l_type=$(this).attr("type")
    l_index=$(this).parent().parent().parent().attr("data-index")
    combien=$(this).next().text()
    $.ajax({
        url: "/helper/email_retraitent/",
        type: "post",
        dataType:"json",
        data: {
            'num':num,
            'type':l_type
        },
        beforeSend: function () {
        // 禁用按钮防止重复提交
            toastr.warning('En cours d\'envoi')
         },
        success: function (res) {
            if(l_type=="venue_imminente"){
                $('#list').bootstrapTable('updateCellByUniqueId', {id: num,field: 'venue_imminente',value: parseInt(combien)+1});
            }else if(l_type=="email_confirmer"){
                $('#list').bootstrapTable('updateCellByUniqueId', {id: num,field: 'situation',value: 'Confirmé'});
                $('#list').bootstrapTable('updateCellByUniqueId', {id: num,field: 'email_confirmer',value: parseInt(combien)+1});
            }else if(l_type=="email_non_confirmer"){
                $('#list').bootstrapTable('updateCellByUniqueId', {id: num,field: 'situation',value: 'Refusé'});
                $('#list').bootstrapTable('updateCellByUniqueId', {id: num,field: 'email_non_confirmer',value: parseInt(combien)+1});
            }
            toastr.success('Email envoyé')
        },
        error: function (data) {
            toastr.error('Échec d\'envoi')
        }
    });
})
function email_confirmer(value, row, index) {
        if(value){
            return '<a class="nav-link">\n' +
            '          <i class="fas fa-envelope text-warning" id="email_retraitent" type="email_confirmer" num="'+row.id+'" style="font-size: 2rem; cursor: pointer"></i>\n' +
            '          <span class="badge badge-danger">'+value+'</span>\n' +
            '        </a>'
        }else{
           return '<a class="nav-link">\n' +
            '          <i class="fas fa-envelope text-warning" id="email_retraitent" type="email_confirmer" num="'+row.id+'"  style="font-size: 2rem; cursor: pointer"></i>\n' +
            '          <span class="badge badge-danger">'+0+'</span>\n' +
            '        </a>'
        }
  }

function email_non_confirmer(value, row, index) {
        if(value){
            return '<a class="nav-link">\n' +
            '          <i class="fas fa-envelope text-warning" id="email_retraitent" type="email_non_confirmer" num="'+row.id+'" style="font-size: 2rem; cursor: pointer"></i>\n' +
            '          <span class="badge badge-danger">'+value+'</span>\n' +
            '        </a>'
        }else{
           return '<a class="nav-link">\n' +
            '          <i class="fas fa-envelope text-warning" id="email_retraitent" type="email_non_confirmer" num="'+row.id+'"  style="font-size: 2rem; cursor: pointer"></i>\n' +
            '          <span class="badge badge-danger">'+0+'</span>\n' +
            '        </a>'
        }
  }

function situation(value, row, index) {
    if(value=='Annulé par la personne'){
         res=value+'<br><i class="far fa-handshake text-warning" index="'+index+'" num="'+row.id+'"  id="click_situation" style="font-size: 2rem;cursor: pointer"></i>'
        return res
    }else{
        return value
    }
}

$('body').on('click','#click_situation',function () {
        var l_index= $(this).attr("index")
        var num= $(this).attr("num")
        $.ajax({
            url: "/helper/situation/",
            type: "post",
            dataType:"json",
            data: {
                num:num,
            },
            success: function (res) {
                if(res){
                    $('#list').bootstrapTable('updateCellByUniqueId', {id: num,field: 'situation',value:'Refusé'});
                }
            }
        });
    })

function data_fr_list(value, row, index){
    if(value) {
        if (value.indexOf(":") != -1) {
            datetime_arr = value.split(' ')
            date_arr = datetime_arr[0].split('-')
            return date_arr[2] + "-" + date_arr[1] + "-" + date_arr[0] + " " + datetime_arr[1]
        } else {
            date_arr = value.split('-')
            return date_arr[2] + "-" + date_arr[1] + "-" + date_arr[0]
        }
    }
  }

function naissance(value, row, index) {
    if(row.naissance) {
        if (row.date_arrive && row.date_depart) {
            myDate = new Date();
            year = myDate.getFullYear();
            value_arr = value.split("-")
            date_arrive = row.date_arrive
            date_depart = row.date_depart
            nait_cette_annee = year + "-" + value_arr[1] + "-" + value_arr[2]
            age = parseInt(year) - parseInt(value_arr[0])
            if (nait_cette_annee >= date_arrive && nait_cette_annee <= date_depart) {
                return '<span class="text-red"><i class="fas fa-birthday-cake"></i>' + fr_date(value) + '<span class="badge badge-danger" style="margin-left: 0.5rem">' + age + '</span></span>'
            } else {
                return '<span>' + fr_date(value) + '<span class="badge badge-danger" style="margin-left: 0.5rem">' + age + '</span></span>'
            }

        } else {
            return value
        }
    }else{
        return value
    }
}


function email(value, row, index) {
    return '<span class="text-primary" style="cursor: pointer" id="envoyer_email">'+value+'<span>'
}

$("body").on("click",'#envoyer_email',function () {
    $('#email').modal('show')
    $('#mode_email').val($(this).text())
    $.ajax({
        url: "/helper/base_email/",
        type: "post",
        dataType:"json",
        data: {
        },
        success: function (res) {
            $('#contenu_email').val(res)
            tinymce.init({
            selector: '#contenu_email',
            setup: function (editor) {
                editor.on('change', function (e) {
                    editor.save();
                });
            },
            menubar: false,
            height:300,
            max_height: 600,
            width: '100%',
            //menubar: 'file edit insert view format table tools help example',
            plugins: "image autolink  code example media autoresize link preview emailtag",
            toolbar: 'undo redo | styleselect | bold italic | alignleft aligncenter alignright | code link example preview emailtag',
            //extended_valid_elements: 'script[language|type|src]',
            contextmenu: "image imagetools table",
            convert_urls: false
        });
        }
    });
})

$("body").on("click",'#btn_envoyer_email',function () {
    adresse=$('#mode_email').val()
    subjet=$('#mode_subjet').val()
    contenu=$('#contenu_email').val()
    $.ajax({
        url: "/helper/envoyer_email/",
        type: "post",
        dataType:"json",
        data: {
            'adresse':adresse,
            'subjet':subjet,
            'contenu':contenu
        },
            success: function (res) {
            toastr.success('Email envoyé')
        },
        error: function (data) {
            toastr.error('Échec d\'envoi')
        }
    });
       })

$('body').on("click",'#click_arrive_partir',function () {
   l_val= $(this).attr("val")
   l_type= $(this).attr("type")
    l_index= $(this).attr("index")
    num= $(this).attr("num")
    $.ajax({
        url: "/helper/arrive_partir/",
        type: "post",
        dataType:"json",
        data: {
            num:num,
            val:l_val,
            type:l_type
        },
        success: function (res) {
            if(res){
                $('#list').bootstrapTable('updateCellByUniqueId', {id: num,field: l_type,value:parseInt(l_val)});
            }
        }
    });
})

function complet(value, row, index) {
        if(value){
           res='<i class="fas fa-battery-full text-danger" index="'+index+'" num="'+row.id+'" id="click_complet"  style="font-size: 2rem;cursor: pointer"></i>'
        }else{
            res=''
        }
        return res
  }

$('body').on("click",'#click_complet',function () {
    l_index= $(this).attr("index")
    num= $(this).attr("num")
    $.ajax({
        url: "/helper/complet/",
        type: "post",
        dataType:"json",
        data: {
            num:num,
        },
        success: function (res) {
            if(res){
                $('#list').bootstrapTable('updateCellByUniqueId', {id: num,field: 'complet',value:''});
            }
        }
    });
})
function limit_width(value,row,index) {
    return '<div class="limit-width">'+value+'</div>'
}


//筛选

var fin_start=''
var fin_end=''
var fin_id=''
$('#toolbar').on('change',"#id_activites,#id_groupes,#id_start,#id_end",function () {
    l_id=$(this).attr('id')
    titre_activite=""
    if(l_id=="id_activites"){
        fin_id=parseInt($(this).val())
        $("#id_groupes").val(0)
    }else if(l_id=="id_groupes"){
         fin_id=parseInt($(this).val())
        $("#id_activites").val(0)
    }else {
        un_id_activite=$("#id_activites").val()
        un_id_groupe=$("#id_groupes").val()
        console.log(un_id_groupe)
        if(un_id_activite!=0){
            fin_id=un_id_activite
        }else if(un_id_groupe!=0){
            fin_id=un_id_groupe
        }else{
            fin_id=0
        }
    l_start=$("#id_start").val()
    l_end=$("#id_end").val()
        if(l_start && l_end){
            l_start=fr_date(l_start)
            l_end=fr_date(l_end)
            if(l_end>=l_start){
                fin_start=l_start
                fin_end=l_end
            }
        }
    }
    flier_by(fin_id,fin_start,fin_end)
})

var data_filter=[]


function flier_by(id,start,end){
    $("#fliter_tool").show()
    if(parseInt(id)!=0){
        data_filter=[]
        $('#list').bootstrapTable('filterBy',{activite:id},{'filterAlgorithm': function(row,filters) {
                if (row.activite == id) {
                    data_filter.push(row)
                    return true
                } else {
                    return false;
                }
            }
        })
    }else{
        data_filter=[]
        $("#fliter_tool").hide()
        $('#list').bootstrapTable('filterBy', {});
    }
    if(start && end && end>=start){
       $("#fliter_tool").show()
        data_filter=[]
        $('#list').bootstrapTable('filterBy',{activite:id},{'filterAlgorithm': function(row,filters){
            if(id>0){
                if(dans_tot_tard(start+' 00:00:00',end+' 23:59:00',row.date_arrive,row.date_depart)&& row.activite==id){
                    data_filter.push(row)
                    return true
                }else{
                    return false;
                }
            }else{
                if(dans_tot_tard(start+' 00:00:00',end+' 23:59:00',row.date_arrive,row.date_depart)){
                    data_filter.push(row)
                    return true
                }else{
                    return false;
                }
            }
        }})
    }
}
$("#tous_confirmer").click(function () {
    l_email=$("#id_emails").val()
    for(x in data_filter){
        envoyer_email_confirmation (data_filter[x],l_email)
    }
})

function envoyer_email_confirmation (value,email) {
    $.ajax({
            url: "/helper/tous_envoyer/",
            type: "post",
            dataType:"json",
            data: {
                'num':value.id,
                'email':email
            },
            success: function (res) {
                toastr.success('Vous avez réussi à envoyer email à '+value.prenom)
            },
            fail:function (res) {
                toastr.error('Vous n\'avez pas réussi à envoyer email à '+value.prenom +', ressayer')
            },
            error: function (data) {
                toastr.error('Vous n\'avez pas réussi à envoyer email à '+value.prenom +', ressayer')
            }
        });
}

//printer
$("body").on('click','#imprimer_list',function () {
    imprimer_data=[]
    $('#printer_list').bootstrapTable('destroy');
    $('#printer').modal()
    num=$(this).attr('num')
    if(parseInt(num)>0){
        $.ajax({
                url: "/helper/imprimer/",
                type: "post",
                dataType:"json",
                data: {
                    'num':num,
                },
                success: function (data) {
                    imprimer_list(data)
                }
            });
    }else{
         $.ajax({
                url: "/helper/chamrbes/",
                type: "post",
                dataType:"json",
                data: {
                    'lieu':'Toutes',
                },
                success: function (data) {
                    print_tous_les_chamrbe(data)
                }
            });
    }
})
function print_tous_les_chamrbe(chambres){
    x=0;
    columns=[]
    columns.push({field: 'chambre', title:'Chambres',sortable: 'true',formatter:'touts_chambre'})
    columns.push({field: 'lieu', title:'Lieu',sortable: 'true'})
    columns.push({field: 'prenom', title:'Prénom',sortable: 'true'})
    columns.push({field: 'nom', title:'Nom',sortable: 'true'})
    for(x in chambres){
        chercher_prenom_arr(chambres[x].lieu,chambres[x].numero)
    }
    $('#printer_list').bootstrapTable({
            pagination: false,
            columns: columns,
            data: imprimer_data,
           // showColumns:true,
        showExport:true,
        })
}

function chercher_prenom_arr(lieu,numero) {
    x=0;
    si=false;
    new_data_filter=JSON.parse(JSON.stringify(data_filter))
    for (x in new_data_filter){
        chambres=JSON.parse(new_data_filter[x].chambre)
        y=0
        for (y in chambres){
            if(chambres[y].lieu==lieu && chambres[y].numero==numero){
                imprimer_data.push({chambre:chambres[y].numero,lieu:chambres[y].lieu,prenom:new_data_filter[x].prenom,nom:new_data_filter[x].nom,lit_matela:chambres[y].lit_matela})
                si=true
            }
        }
        parents=JSON.parse(new_data_filter[x].parent)
        z=0
        if( new_data_filter[x].parent && new_data_filter[x].parent.length>0){
        for(z in parents){
            chambres_parent=parents[z].chambre
            m=0
                for(m in chambres_parent){
                    if(chambres_parent[m].lieu==lieu && chambres_parent[m].numero==numero){
                        imprimer_data.push({chambre:chambres_parent[m].numero,lieu:chambres_parent[m].lieu,prenom:parents[z].prenom,lit_matela:chambres_parent[m].lit_matela})
                        si=true
                    }
            }
        }
        }
    }
    if(!si){
        imprimer_data.push({chambre:numero,lieu:lieu,prenom:'',lit_matela:''})
    }
}

function touts_chambre(value, row, index) {
     return  '<i class="'+row.lit_matela+'"></i>'+value
}

var imprimer_data=[]
function imprimer_list(data) {
    //标题头
    id_activites=$("#id_activites option:selected").text()
    id_groupe=$("#id_groupes option:selected").text()
    l_start=$("#id_start").val()
    l_end=$("#id_end").val()
    if(id_activites=="Tous"){
        id_activites=""
    }
    if(id_groupe=="Tous"){
        id_groupe=""
    }
    if(l_start && l_end){
        start_end=' '+l_start+' / '+l_end
    }else{
        start_end=""
    }
    $("#print_titre").text(id_activites+id_groupe+start_end)
    //列表
    imprimer_data=[]
    $('#textarea1').html('')
    $('#textarea2').html('')


    if(data.type=="Détail"){
        $("#row_table").hide()
        for(xs in data_filter){
            $('#textarea1').append(textarea_detail(data.textarea1,data_filter[xs])+'<div style="page-break-after:always;"></div>')
        }

    }else if(data.type=="Liste"){
        $("#row_table").show()
        $('#textarea1').append(textarea(data.textarea1,data_filter))
        $('#textarea2').append(textarea(data.textarea2,data_filter))
        list=JSON.parse(data.list)
    list_table=list.table
    columns=[]
    for(x in list_table){
        columns.push({field: list_table[x][1], title:list_table[x][0],sortable: 'true'})
    }
    columns[0]['cellStyle']='un_couleur'
    if(columns[0]['field']!='chambre'){
            if(columns[0]['field']=='chambre'){
                columns[0]['formatter']='print_chambre'
            }
    }else{
        columns.splice(1, 0, {field: 'lieu', title:'Lieu',sortable: 'true'});
    }

    for(m in columns){
        if(columns[m]['field']=='repas'){
            columns[m]['formatter']='repas'
        }else if(columns[m]['field']=='parent'){
            columns[m]['formatter']='parent'
        }else if(columns[m]['field']=='naissance'){
            columns[m]['formatter']='naissance'
        }else if(columns[m]['field']=='date_arrive'){
            columns[m]['formatter']='data_fr_list'
        }else if(columns[m]['field']=='date_depart'){
            columns[m]['formatter']='data_fr_list'
        }else if(columns[m]['field']=='date1'){
            columns[m]['formatter']='data_fr_list'
        }else if(columns[m]['field']=='date2'){
            columns[m]['formatter']='data_fr_list'
        }else if(columns[m]['field']=='datetime1'){
            columns[m]['formatter']='data_fr_list'
        }else if(columns[m]['field']=='datetime2'){
            columns[m]['formatter']='data_fr_list'
        }
    }
    if(list_table[0][1]=='chambre'){
        new_fliter=[]
         for(y in data_filter){
             data_fliter_sans(data_filter[y],JSON.parse(data_filter[y].chambre))
             tr_parent(data_filter[y],JSON.parse(data_filter[y].parent))
        }

        $('#printer_list').bootstrapTable({
            pagination: false,
              columns: columns,
              data: imprimer_data,
            showColumns:true,
            showExport:true,
            sortName:list.ordre1,
            })
    }else{
        $('#printer_list').bootstrapTable({
            pagination: false,
            columns: columns,
            data: data_filter,
            showColumns:true,
            showExport:true,
            sortName:list.ordre1,
        })
    }
    }
}

function un_couleur(value, row, index) {
    return {css: {"background-color": row.couleur+" !important"}}
}

function print_chambre(value, row, index) {
 return tr_chambre(JSON.parse(value))
}

function data_fliter_sans(row,chambre) {
    var new_row=new Object()
    $.extend(new_row,row);
    new_row.chambre=tr_chambre(chambre)
    new_row.lieu=tr_lieu(chambre)
    imprimer_data.push(new_row)
}
function tr_parent(row,parent) {
    for (un in parent){
        tr_parent_change(row,parent[un])
    }
}

function tr_parent_change(row,parent){
     var new_row=new Object()
    $.extend(new_row,row);
    new_row['chambre']=tr_chambre(parent.chambre)
    new_row['lieu']=tr_lieu(parent.chambre)
    new_row['prenom']=parent.prenom
    new_row['nom']=parent.nom
    new_row['naissance']=fr_date(parent.naissance)
    new_row['sex']=parent.relation
    imprimer_data.push(new_row)
}

function tr_chambre(chambres) {
    la_numero=[]
    cc=0
    for (cc in chambres){
        l_res='<i class="'+chambres[cc].lit_matela+'"></i>'+chambres[cc].numero
        la_numero.push(l_res)
    }
        return la_numero.join(', ')
}

function tr_lieu(chambres) {
    la_numero=[]
    cc=0
    for (cc in chambres){
        la_numero.push(chambres[cc].lieu)
    }
        return la_numero.join(', ')
}
function textarea_detail(contenu,data){
    var regex3 = /(?<=\{)(.+?)(?=\})/g; // {}
    var champe_text = contenu.match(regex3);
    for(x in champe_text){
        champ_arr=champe_text[x].split("|")
        replace_data=''
        if(data[champ_arr[1]]){
            if(champ_arr[1]=='parent'){
                replace_data=parent(data[champ_arr[1]],0,0)
            }else if(champ_arr[1]=='chambre'){
                replace_data=tr_chambre(JSON.parse(data[champ_arr[1]]))
            }else
                {
                replace_data=data[champ_arr[1]]
            }

        }
        contenu=contenu.replace("{"+champe_text[x]+"}",replace_data)
    }
    return contenu
       }


function textarea(contenu,data) {
    var regex3 = /(?<=\{)(.+?)(?=\})/g; // {}
    var champe_text = contenu.match(regex3);
    for(x in champe_text){
        champ_arr=champe_text[x].split("|")
        contenu=contenu.replace("{"+champe_text[x]+"}",textarea_res(champ_arr,data))
    }
    return contenu
}


function textarea_res(arr,data) {
    values=[]
    for(x in data){
        if(data[x][arr[1]]){
            values.push(data[x][arr[1]])
        }else{
            values.push('')
        }
    }
    if(arr[2]=="Sum"){
        return sum(values)
    }else if(arr[2]=='Average'){
        if(values.length>0){
            return sum(values)/values.length
        }else{
            return ''
        }
    }else {
        return values.join(' ')
    }
}

function sum(arr) {
    var s = 0;
    for (var i=arr.length-1; i>=0; i--) {
        s += parseInt(arr[i]);
    }
    return s;
}

// graphique
si_numbre=['Total','prix','prix1','nombre_garcons','nombre_filles','nombre_hommes','nombre_femmes','nombre_pretre','Age_moyen','pretres_supplementaires','numbre1','numbre2','numbre3']
graphique_database=[]
graphique_database_filter=[]
les_data=[]
original_data=[]
$("body").on('click','#graphique_list',function () {
    $('#graphique_mode').modal()
    l_type=$(this).attr('type')
    l_num=$(this).attr('num')
    $.ajax({
        url: "/helper/graphique/",
        type: "post",
        dataType:"json",
        async:false,
        data: {
            'id':l_num,
        },
        success: function (data1) {
            $("#graphique_title").text(data1.titre)
            graphique_database=data1
            xx=1
            while (xx < 5) {
                if (data1['fliter' + xx]) {
                    $("#filter"+xx+"_radio").show()
                    if (data1['fliter'+xx+'_type'] == 'Texte') {
                        graphique_database_filter.push('Texte')
                        $("#filter"+xx+"_text").show()
                        un1 = '                        <label>' + data1['fliter'+xx+'_name'] + '</label>\n' +
                            '                        <input type="text" class="form-control" placeholder="Enter ...">\n'
                    } else if(data1['fliter'+xx] == 'arrive' || data1['fliter'+xx] == 'partir' || data1['fliter'+xx] == 'venue_imminente_reponse') {
                        graphique_database_filter.push('Select')
                        un1 = '<label>' + data1['fliter'+xx+'_name'] + '</label>\n' +
                            '                        <select class="form-control">\n'
                         un1+= ' <option value="">------</option>\n'+' <option value="0">Non</option>\n'+' <option value="1">Oui</option>\n'
                           un1+= '</select>'
                    }
                else if(data1['fliter'+xx+'_type'] == 'Select' && data1['fliter'+xx] != 'arrive' && data1['fliter'+xx] != 'partir' && data1['fliter'+xx] != 'venue_imminente_reponse') {
                        graphique_database_filter.push('Select')
                        un1 = '<label>' + data1['fliter'+xx+'_name'] + '</label>\n' +
                            '                        <select class="form-control" id="avec_parent">\n'
                         un1+= ' <option value="">------</option>\n'
                        choix=data1['fliter'+xx+'_choix'].split(',')
                        for (yy in choix){
                            un1+= ' <option value="'+choix[yy]+'">'+choix[yy]+'</option>\n'
                        }
                           un1+= '</select>'
                    }
                else{
                        graphique_database_filter.push('Number')
                        $("#filter"+xx+"_numbre").show()
                        un1 = '                        <label>' + data1['fliter'+xx+'_name'] + '</label>\n' +
                            '                        <input type="number" class="form-control" placeholder="Enter ...">\n'
                    }
                    $("#filter" + xx).html(un1)
                }else{
                    graphique_database_filter.push('')
                }
                xx += 1
            }
            graphique_datas(data1,data1.avec_parent,false,[])
        }
    });
})

function graphique_datas(data1,avec_parent,fliter,le_new_datas) {
    if(graphique_database['value']=='repas'){
        //repas
        labels_pdej = []
        values_pdej = {}
        labels_dej = []
        values_dej = {}
        labels_din = []
        values_din = {}
        if (!fliter) {
            les_data = graphique_data(JSON.parse(JSON.stringify(data_filter)), avec_parent)
            original_data = les_data
        } else {
            les_data = le_new_datas
        }
        for (x in les_data){
            if(les_data[x].repas){
                les_repas=JSON.parse(les_data[x].repas)
                for(y in les_repas){
                    if(les_repas[y].indexOf('pdej')>=0) {
                        le_repas_date=les_repas[y].replace('pdej',"")
                        le_repas_date=date_reduire(le_repas_date,graphique_database.value_x_date)
                        if ($.inArray(le_repas_date, labels_pdej) < 0) {
                            labels_pdej.push(le_repas_date)
                            if(avec_parent && les_data[x].parent){
                                values_pdej[le_repas_date]=1
                            }else{
                                values_pdej[le_repas_date]=les_data[x].Total
                            }
                        } else {
                            if(avec_parent && les_data[x].parent){
                                values_pdej[le_repas_date] = values_pdej[le_repas_date] + 1
                            }else{
                                values_pdej[le_repas_date] = values_pdej[le_repas_date] + les_data[x].Total
                            }
                        }
                    }else
                    if(les_repas[y].indexOf('dej')>=0 && les_repas[y].indexOf('pdej')<0) {
                        le_repas_date=les_repas[y].replace('dej',"")
                        le_repas_date=date_reduire(le_repas_date,graphique_database.value_x_date)
                        if ($.inArray(le_repas_date, labels_dej) < 0) {
                            labels_dej.push(le_repas_date)
                            if(avec_parent && les_data[x].parent){
                                values_dej[le_repas_date]=1
                            }else{
                                values_dej[le_repas_date]=les_data[x].Total
                            }
                        } else {
                            if(avec_parent && les_data[x].parent){
                                values_dej[le_repas_date] = values_dej[le_repas_date] + 1
                            }else{
                                values_dej[le_repas_date] = values_dej[le_repas_date] + les_data[x].Total
                            }
                        }
                    }else
                    if(les_repas[y].indexOf('din')>=0) {
                        le_repas_date=les_repas[y].replace('din',"")
                        le_repas_date=date_reduire(le_repas_date,graphique_database.value_x_date)
                        if ($.inArray(le_repas_date, labels_din) < 0) {
                            labels_din.push(le_repas_date)
                            if(avec_parent && les_data[x].parent){
                                values_din[le_repas_date]=1
                            }else{
                                values_din[le_repas_date]=les_data[x].Total
                            }
                        } else {
                            if(avec_parent && les_data[x].parent){
                                values_din[le_repas_date] = values_din[le_repas_date] + 1
                            }else{
                                console.log(les_data[x].id)
                                values_din[le_repas_date] = values_din[le_repas_date] + les_data[x].Total
                            }
                        }
                    }
                }
            }
        }
        repas_date = $.merge(labels_pdej,labels_dej);
        repas_date = $.merge(repas_date,labels_din);
        repas_date = repas_date.sort();
        repas_date=$.unique(repas_date);
        values_pdej_fin=[]
        values_dej_fin=[]
        values_din_fin=[]
        for(m in repas_date){
            if(values_pdej.hasOwnProperty(repas_date[m])){
                values_pdej_fin.push(values_pdej[repas_date[m]])
            }else{
                 values_pdej_fin.push(0)
            }
            if(values_dej.hasOwnProperty(repas_date[m])){
                values_dej_fin.push(values_dej[repas_date[m]])
            }else{
                 values_dej_fin.push(0)
            }
            if(values_din.hasOwnProperty(repas_date[m])){
                values_din_fin.push(values_din[repas_date[m]])
            }else{
                 values_din_fin.push(0)
            }
        }
        if (myChart != null) {
             updatemyChart_repas(repas_date,['Petit-déjeuner','Déjeuner','Dîner'] ,[values_pdej_fin,values_dej_fin,values_din_fin])
        } else {
             faire_graphique_repas(repas_date,['Petit-déjeuner','Déjeuner','Dîner'] ,[values_pdej_fin,values_dej_fin,values_din_fin])
        }
    }else {
        labels = []
        values = []
        counts = []
        if (!fliter) {
            les_data = graphique_data(data_filter, avec_parent)
            original_data = les_data
        } else {
            les_data = le_new_datas
        }
        for (x in les_data) {
            if ($.inArray(les_data[x][data1.value_x], labels) < 0) {
                labels.push(les_data[x][data1.value_x])
                if (data1.value_compter == 'Sum') {
                    values.push(les_data[x][data1.value])
                } else if (data1.value_compter == 'Average') {
                    values.push(les_data[x][data1.value])
                    counts.push(1)
                } else {
                    values.push(1)
                }
            } else {
                l_index = $.inArray(les_data[x][data1.value_x], labels)
                if (data1.value_compter == 'Sum') {
                    if (!les_data[x][data1.value]) {
                        values[l_index] = values[l_index]
                    } else {
                        values[l_index] = values[l_index] + les_data[x][data1.value]
                    }
                } else if (data1.value_compter == 'Average') {
                    counts[l_index] = counts[l_index] + 1
                    if (!les_data[x][data1.value]) {
                        values[l_index] = values[l_index]
                    } else {
                        values[l_index] = values[l_index] + les_data[x][data1.value]
                    }
                } else {
                    values[l_index] = values[l_index] + 1
                }
            }
        }
        if (data1.value_compter == 'Average') {
            for (m in values) {
                values[m] = values[m] / counts[m]
            }
        }
        if (myChart != null) {
            updatemyChart(data1.type, labels, values)
        } else {
            faire_graphique(data1.type, labels, values)
        }
    }
}


function graphique_data(data,avec_parent) {
    new_data=data
    for (x in new_data){
        if(graphique_database['value_x_date'] && graphique_database['value_x']!='repas'&& graphique_database['value']!='repas'){
            new_data[x][graphique_database['value_x']]=date_reduire(new_data[x][graphique_database['value_x']],graphique_database['value_x_date'])
        }
        new_data[x]['age']=Age(new_data[x].naissance,false)
        if(avec_parent) {
            if (new_data[x].parent) {
                parents = JSON.parse(new_data[x].parent)
                for (y in parents) {
                    new_un_data = JSON.parse(JSON.stringify(new_data[x]))
                    new_un_data['nom'] = parents[y].nom
                    new_un_data['prenom'] = parents[y].prenom
                    new_un_data['naissance'] = parents[y].naissance
                    new_un_data['sex'] = 'Homme'
                    new_un_data['age'] = Age(parents[y].naissance, true)
                    if (parents[y].relation == 'Fils' || parents[y].relation == 'Conjoint') {
                        new_un_data['sex'] = 'Homme'
                    } else {
                        new_un_data['sex'] = 'Femme'
                    }
                    for (z in si_numbre) {
                        new_un_data[si_numbre[z]] = 0
                    }
                    new_data.push(new_un_data)
                }
            }
        }
    }
    return new_data
}

function faire_graphique_repas(labels,titles,values) {
    var ctx = document.getElementById('myChart');
    datas=[]
    for(x in values){
        datas.push({data:values[x],label:titles[x],backgroundColor:randomColorGenerator()})
    }
         myChart = new Chart(ctx, {
            type: 'bar',
             plugins: [{
                beforeInit: function(chart, options) {
                  chart.legend.afterFit = function() {
                    this.height = this.height + 50;
                  };
                }
              }],
            data: {
                labels: labels,
                datasets: datas
            },
            options: {
                legend: {
                    labels:{

                    },
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                },
                hover: {
                    animationDuration: 0  // 防止鼠标移上去，数字闪烁
                },
                animation: {           // 这部分是数值显示的功能实现
                    onComplete: function () {
                        var chartInstance = this.chart,
                        ctx = chartInstance.ctx;
                        // 以下属于canvas的属性（font、fillStyle、textAlign...）
                        ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
                        ctx.fillStyle = "black";
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'bottom';
                        this.data.datasets.forEach(function (dataset, i) {
                            var meta = chartInstance.controller.getDatasetMeta(i);
                            meta.data.forEach(function (bar, index) {
                                var data = dataset.data[index];
                                ctx.fillText(data, bar._model.x, bar._model.y - 5);
                            });
                        });
                    }
            }

            }
        });
}

function updatemyChart_repas(labels,titles,values){
    datas=[]
    for(x in values){
        datas.push({data:values[x],label:titles[x],backgroundColor:randomColorGenerator()})
    }
    myChart.data.datasets = datas;
    myChart.update();
}

function date_reduire(value,type) {
    if(value){
        if(value.indexOf(' ')>0){
            arr_datetime=value.split(' ')
            arr_date=arr_datetime[0].split('-')
        }else{
            arr_date=value.split('-')
        }
        if(type=='Par mois'){
            return arr_date[0]+'-'+arr_date[1]
        }else if(type=='Par an'){
            return arr_date[0]
        }else {
            return arr_date[0]+'-'+arr_date[1]+'-'+arr_date[2]
        }
    }
}

var randomColorGenerator = function () {
    return '#' + (Math.random().toString(16) + '0000000').slice(2, 8);
};

var myChart=null;
function faire_graphique(l_type,labels,values) {
    if(myChart!=null){
        myChart.destroy();
    }
    new_labels=JSON.parse(JSON.stringify(labels))
    new_values=[]
    new_labels.sort(function(a,b){
        return a-b;
})
    console.log(new_labels)
    for(x in new_labels){
        for(y in labels){
            if(new_labels[x]==labels[y]){
                new_values.push(values[y])
            }
        }
    }
    if (JSON.stringify(new_labels)==JSON.stringify([0,1])){
        new_labels=["Oui","Non"]
    }
    if(l_type=='Graphique circulaire') {
        var ctx = document.getElementById('myChart');
         myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
            labels: new_labels,
            datasets: [
                {
                    data: new_values,
                    backgroundColor: labels.map(function(hex) {
                        return randomColorGenerator();
                    }),
                }
            ]
        },

            options: {
            legend: {
                display: true
            }
        }
        })
    }else {
        var ctx = document.getElementById('myChart');
         myChart = new Chart(ctx, {
            type: 'bar',
             plugins: [{
                beforeInit: function(chart, options) {
                  chart.legend.afterFit = function() {
                    this.height = this.height + 50;
                  };
                }
              }],
            data: {
                labels: new_labels,
                datasets: [{
                    // label: 'value',
                    data: new_values,
                    backgroundColor: labels.map(function(hex) {
                        return randomColorGenerator();
                    }),
                }]
            },
            options: {
                legend: {
                    display: false
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                },
                hover: {
                    animationDuration: 0  // 防止鼠标移上去，数字闪烁
                },
                animation: {           // 这部分是数值显示的功能实现
                    onComplete: function () {
                        var chartInstance = this.chart,
                        ctx = chartInstance.ctx;
                        // 以下属于canvas的属性（font、fillStyle、textAlign...）
                        ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
                        ctx.fillStyle = "black";
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'bottom';
                        this.data.datasets.forEach(function (dataset, i) {
                            var meta = chartInstance.controller.getDatasetMeta(i);
                            meta.data.forEach(function (bar, index) {
                                var data = dataset.data[index];
                                ctx.fillText(data, bar._model.x, bar._model.y - 5);
                            });
                        });
                    }
            }
            }
        });
    }
}

function updatemyChart(l_type,labels,values){
    new_labels=JSON.parse(JSON.stringify(labels))
    new_values=[]
    new_labels.sort()
    for(x in new_labels){
        for(y in labels){
            if(new_labels[x]==labels[y]){
                new_values.push(values[y])
            }
        }
    }
    myChart.data.datasets[0].data = new_values;
    myChart.update();
}

function Age(value,fr) {
    if(fr){
       value= fr_date(value)
    }
    if(value) {
        myDate = new Date();
        year = myDate.getFullYear();
        value_arr = value.split("-")
        nait_cette_annee = year + "-" + value_arr[1] + "-" + value_arr[2]
        age = parseInt(year) - parseInt(value_arr[0])
        return age
    }else{
        return 0
    }
}

$("#graphique_valide").click(function () {
    filter_contenu=[]
    for(x in graphique_database_filter){
        if(graphique_database_filter[x]=='Select'){
            m=parseInt(x)+1
            l_value=$("#filter"+m).children('select').val()
            logic=$("input[name='filter"+m+"_radio']:checked").val()
            filter_contenu.push({field:graphique_database['fliter'+m],value:l_value,compte:'=',logic:logic})
        }else if(graphique_database_filter[x]=='Number'){
             m=parseInt(x)+1
            l_value=$("#filter"+m).children('input').val()
            logic=$("input[name='filter"+m+"_radio']:checked").val()
            compte=$("#filter"+m+"_numbre").children('select').val()
            filter_contenu.push({field:graphique_database['fliter'+m],value:l_value,compte:compte,logic:logic})
        }else{
             m=parseInt(x)+1
            l_value=$("#filter"+m).children('input').val()
            logic=$("input[name='filter"+m+"_radio']:checked").val()
            compte=$("#filter"+m+"_text").children('select').val()
            filter_contenu.push({field:graphique_database['fliter'+m],value:l_value,compte:compte,logic:logic})
        }
    }
    le_new_data=[]
    console.log(filter_contenu)
    for(y in original_data){
        logic=true
        for(z in filter_contenu){
            if(filter_contenu[z]['value']) {
                if(filter_contenu[z]['logic']=='ou') {
                    if (filter_contenu[z]['compte'] == '=') {
                        logic |= original_data[y][filter_contenu[z]['field']] == filter_contenu[z]['value']

                    } else if (filter_contenu[z]['compte'] == 'include') {
                        logic |= original_data[y][filter_contenu[z]['field']].indexOf(filter_contenu[z]['value']) >= 0
                    } else if (filter_contenu[z]['compte'] == 'exclude') {
                        logic |= original_data[y][filter_contenu[z]['field']].indexOf(filter_contenu[z]['value']) <= 0
                    } else {
                        logic |= eval(original_data[y][filter_contenu[z]['field']] + filter_contenu[z]['compte'] + filter_contenu[z]['value'])
                    }
                }else{
                    if (filter_contenu[z]['compte'] == '=') {
                        logic &= original_data[y][filter_contenu[z]['field']] == filter_contenu[z]['value']

                    } else if (filter_contenu[z]['compte'] == 'include') {
                        logic &= original_data[y][filter_contenu[z]['field']].indexOf(filter_contenu[z]['value']) >= 0
                    } else if (filter_contenu[z]['compte'] == 'exclude') {
                        logic &= original_data[y][filter_contenu[z]['field']].indexOf(filter_contenu[z]['value']) <= 0
                    } else {
                        logic &= eval(original_data[y][filter_contenu[z]['field']] + filter_contenu[z]['compte'] + filter_contenu[z]['value'])
                    }
                }
            }
        }
        if(logic) {
            le_new_data.push(original_data[y])
        }
    }
    graphique_datas(graphique_database,graphique_database['avec_parent'],true,le_new_data)
})

$("#printer_contenu").click(function () {
    //$("#printer_body").find("#row_table").removeClass('table_hide')
    // $("#printer_body").find(".fixed-table-toolbar").hide()
    $("#printer_body").jqprint({
     debug:false, //如果是true则可以显示iframe查看效果（iframe默认高和宽都很小，可以再源码中调大），默认是false
     printContainer: true, //表示如果原来选择的对象必须被纳入打印（注意：设置为false可能会打破你的CSS规则）。
     operaSupport: false//表示如果插件也必须支持歌opera浏览器，在这种情况下，它提供了建立一个临时的打印选项卡。默认是true
});
})


