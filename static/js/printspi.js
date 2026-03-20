function imprimer_list(printe,data){
    $('#textarea1_print').html("")
    $('#textarea2_print').html("")
    $('#print_table_row').hide()
    console.log(data)
    if(printe.type=="Détail"){
        for(x in data){
            $('#textarea1_print').append(textarea_detail(printe.textarea1+'<div class="printfoot">'+printe.textarea2+'</div>',data[x],'Détail')+'<div style="page-break-after:always;"></div>')
        }
    }else if(printe.type=="Liste"){
        $('#textarea1_print').append(textarea_detail(printe.textarea1,data,'liste'))
        $('#spi_print').append(print_list(printe.list,data))
        $('#textarea2_print').append(textarea_detail(printe.textarea2,data,'liste'))
    }
}

function envoyer_list(printe,data) {
    console.log(data)
    if(printe.type=="Détail"){
        for(x in data){
            l_email=data[x].email
            nom=data[x].nom
            contenu=textarea_detail(printe.textarea1+'<div class="printfoot">'+printe.textarea2+'</div>',data[x],'Détail')+'<div style="page-break-after:always;"></div>'
            $.ajax({
                url: "/helper/envoyer_tous/",
                type: "post",
                dataType:"json",
                data: {
                    'contenu':contenu,
                    'subjet':printe.titre,
                    'email':l_email,
                },
                beforeSend: function () {
                    // 禁用按钮防止重复提交
                toastr.warning('En cours d\'envoi à ' +nom)
                },
                success: function (data) {
                    toastr.success('Email envoyé à '+nom)
                },
                error: function (data) {
                    toastr.error('Échec d\'envoi à '+nom)
                }
            });
        }
    }else if(printe.type=="Liste"){
        contenu=textarea_detail(printe.textarea1,data,'liste')+print_list(printe.list,data)+textarea_detail(printe.textarea2,data,'liste')

    }
}

function textarea_detail(contenu,data,type){
    var regex3 = /(?<=\{)(.+?)(?=\})/g; // {}
    var champe_text = contenu.match(regex3);
    for(x in champe_text){
        champ_arr=champe_text[x].split("|")
        replace_data=''
        if(type=='liste') {
            if (champ_arr[2] == "Count") {
                replace_data = data.length
            } else if (champ_arr[2] == "Sum") {
                replace_data = 0
                for (m in data) {
                    replace_data += data[m][champ_arr[1]]
                }
                replace_data.toFixed(2)
            } else if (champ_arr[2] == "Average") {
                replace_data = 0
                for (m in data) {
                    replace_data += data[m][champ_arr[1]]
                }
                replace_data=replace_data/data.length
                replace_data.toFixed(2)
            } else {
                replace_data = data[0][champ_arr[1]]
            }
        }else{
            if (champ_arr[1] in data) {
                    replace_data = data[champ_arr[1]]
                }
        }
        contenu=contenu.replace("{"+champe_text[x]+"}",replace_data)
    }
    var regex3 = /(?<=\(\()(.+?)(?=\)\))/g; // {}
    var champe_text = contenu.match(regex3);
    for(y in champe_text){
        champ_arr=champe_text[y].split("||")
        replace_data=''
        if(champ_arr[0]=='calcul'){
            replace_data=eval(champ_arr[1]).toFixed(2)
            contenu=contenu.replace("(("+champe_text[y]+"))",replace_data)
        }
    }
    return contenu
}

function print_list(liste,data) {
    $('#print_table_row').show()
    list = JSON.parse(liste)
    liste = list.table
    columns = []
    new_data = []
    new_row = {}
    for (m in data) {
        for (x in liste) {
            if (liste[x].length==3) {
                if(liste[x][1].indexOf('{')>=0){
                    new_row[liste[x][0]] = list_remplace(liste[x][1],data[m])
                }else{
                    new_row[liste[x][0]] = liste[x][1]
                }
            } else {
                new_row[liste[x][1]] = data[m][liste[x][1]]
            }
        }
        new_data.push(new_row)
}
     console.log(new_data)
    // for(m in data){
    //     console.log(data[m])
    // }
    for(x in liste){
        if(liste[x].length==3){
            columns.push({field: liste[x][0], title:liste[x][0],sortable: 'true'})
        }else{
            columns.push({field: liste[x][1], title:liste[x][0],sortable: 'true'})
        }
    }
    console.log(columns)
    $('#printer_list').bootstrapTable({
        pagination: false,
        columns: columns,
        data: new_data,
        showColumns:true,
        showExport:true,
        sortName:list.ordre1,
    })
}

function calcul(value, row, index) {
    return value
}

function list_remplace(str,data) {
    var regex3 = /(?<=\{)(.+?)(?=\})/g; // {}
    var champe_text = str.match(regex3);
    for(x in champe_text){
        str=str.replace("{"+champe_text[x]+"}",data[champe_text[x]])
    }
    return eval(str).toFixed(2)
}

$("#printer_contenu").click(function () {
    $("#spi_print").find("#row_table").removeClass('table_hide')
    $("#spi_print").find(".fixed-table-toolbar").hide()
    $("#spi_print").jqprint({
        importCSS: true,
     debug:false, //如果是true则可以显示iframe查看效果（iframe默认高和宽都很小，可以再源码中调大），默认是false
     printContainer: true, //表示如果原来选择的对象必须被纳入打印（注意：设置为false可能会打破你的CSS规则）。
     operaSupport: false//表示如果插件也必须支持歌opera浏览器，在这种情况下，它提供了建立一个临时的打印选项卡。默认是true
});
})