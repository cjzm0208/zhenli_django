tinymce.PluginManager.add("myimage",function(a,b){
	a.addButton("myimage",
	{
	text:"My button",
	icon:'media',
	onclick:function(){
		a.windowManager.open({
			title:"TinyMCE site",
			url:b+"/dialog.html",
			width:600,
			height:400,
			buttons:[{
				text:"Insert",
				onclick:function(){var b=a.windowManager.getWindows()[0];a.insertContent(b.getContentWindow().document.getElementById("content").value),b.close()
				},
				},
				{
				text:"Close",
				onclick:"close",
				},
				]
				
		})
		}
	}),
	
	
	});
