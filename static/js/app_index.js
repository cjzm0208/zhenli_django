function fun_app_index_type(value, row, index) {
        var choices_type={'single':'单次显示','loops':'循环','new':'最新','time':'时间显示','time_new':'时间显示如无显示最新'}
    console.log(row)
        if(row.parent__id!=1){
            return choices_type[value]
        }else{
           return "-----"
        }
  }

  function fun_app_index_days(value, row, index) {
    console.log(row)
        if(row.parent__id!=1){
            return value
        }else{
           return "-----"
        }
  }

  function fun_app_index_cathegory(value, row, index) {
    console.log(row)
        if(row.parent__id!=1){
            return value
        }else{
           return "-----"
        }
  }
  $("#id_parent").change(function () {
      if($(this).val()!=1){
          $("#id_title").val($('#id_parent option:selected').text())
          $('#id_title').prop('readonly', true);
      }else{
          $("#id_title").val("")
          $('#id_title').prop('readonly', false);
      }
  })