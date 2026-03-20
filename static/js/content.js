// var textarea_id = 0
// $("#new_contenu_text").click(function () {
//     $("#new_contenu_compo").append('<textarea cols="40" rows="5" class="form-control new_content content_textarea" id="new_content_textarea' + textarea_id + '" placeholder="Contenu" ></textarea>')
//     console.log(textarea_id)
//     tinyMCE.init({selector: '#new_content_textarea' + textarea_id,
//     menubar: false,
//     });
//     // tinymce.execCommand("mceAddControl", false, "#weowe");
//     textarea_id += 1;
// })

function new_content_fun(content_block,readOnly){
    var editor1 = new EditorJS({
      /**
       * Enable/Disable the read only mode
       */
      readOnly: readOnly,

      /**
       * Wrapper of Editor
       */
      holder: 'editorjs',

      /**
       * Common Inline Toolbar settings
       * - if true (or not specified), the order from 'tool' property will be used
       * - if an array of tool names, this order will be used
       */
      // inlineToolbar: ['link', 'marker', 'bold', 'italic'],
      // inlineToolbar: true,

      /**
       * Tools list
       */
      tools: {
        /**
         * Each Tool is a Plugin. Pass them via 'class' option with necessary settings {@link docs/tools.md}
         */
        header: {
          class: Header,
          inlineToolbar: ['bold', 'italic','link'],
          config: {
            placeholder: 'Header'
          },
          shortcut: 'CMD+SHIFT+H'
        },

        /**
         * Or pass class directly without any configuration
         */
        image:NewImage,
        audio:Audio,
        video:Video,

        // image: {
        //   class: ImageTool,
        //   config: {
        //     endpoints: {
        //       byFile: 'http://localhost:8008/uploadFile', // Your backend file uploader endpoint
        //       byUrl: 'http://localhost:8008/fetchUrl', // Your endpoint that provides uploading by Url
        //     }
        //   }
        // },

        // list: {
        //   class: List,
        //   inlineToolbar: true,
        //   shortcut: 'CMD+SHIFT+L'
        // },

        // checklist: {
        //   class: Checklist,
        //   inlineToolbar: true,
        // },

        // quote: {
        //   class: Quote,
        //   inlineToolbar: true,
        //   config: {
        //     quotePlaceholder: 'Enter a quote',
        //     captionPlaceholder: 'Quote\'s author',
        //   },
        //   shortcut: 'CMD+SHIFT+O'
        // },
        //
        // warning: Warning,

        // marker: {
        //   class:  Marker,
        //   shortcut: 'CMD+SHIFT+M'
        // },
        //
        // code: {
        //   class:  CodeTool,
        //   shortcut: 'CMD+SHIFT+C'
        // },
        //
        // delimiter: Delimiter,
        //
        // inlineCode: {
        //   class: InlineCode,
        //   shortcut: 'CMD+SHIFT+C'
        // },
        //
        // linkTool: LinkTool,
        //
        // embed: Embed,

        table: {
          class: Table,
          inlineToolbar: true,
          shortcut: 'CMD+ALT+T'
        },

      },

      /**
       * This Tool will be used as default
       */
      // defaultBlock: 'paragraph',

      /**
       * Initial Editor data
       */
      data: {
        blocks: content_block
      },
      onReady: function(){
        $('video,audio').mediaelementplayer();
        edior_save();
      },
      onChange: function(api, event) {
        // console.log('something changed', event);
        edior_save();
      }
    });


    /**
     * Toggle read-only button
     */
    // const toggleReadOnlyButton = document.getElementById('toggleReadOnlyButton');
    // const readOnlyIndicator = document.getElementById('readonly-state');

    /**
     * Saving example
     */
    function edior_save(){
      editor1.save()
        .then((savedData) => {
            $("#id_new_contenu").val(JSON.stringify(savedData.blocks))
          // cPreview.show(savedData, document.getElementById("output"));
        })
        .catch((error) => {
          // console.error('Saving error', error);
        });
    }
}


var options = [];
$(".modal_cathegorie").each(function(){
    $(this).hide()
  var res='<div class="d-flex row"><div id="show_option_checked">'+$("#cathegorie_checked").html()+'</div><div><button type="button" class="btn btn-primary btn-sm m-1" id="modal_cathegorie_add" data-toggle="modal" data-target="#modal-cathegorie">添加</button></div></div>'
    $(this).parent().append(res)

})

// $("body").on("click","#modal_cathegorie_add",function(){
//   modal()
// })