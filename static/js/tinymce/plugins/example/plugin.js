tinymce.PluginManager.add('example', function(editor, url) {
	var openDialog = function() {
		tinymce.activeEditor.windowManager.openUrl({
			title: 'Les dossiers',
			url: '/tinymc/admin_TinyMCE/',
			width: 1000,
			height: 500,
			buttons: [{
					type: 'custom',
					name: 'action',
					text: 'Submit',
					primary: true,
				},
				{
					type: 'cancel',
					name: 'cancel',
					text: 'Close Dialog'
				}
			],
			onAction: function(instance, trigger) {
				editor.insertContent(mon_message);
				// close the dialog
				//tinymce.ScriptLoader.load('../../../js/mediaelement-and-player.js');
				//$('#youtube').mediaelementplayer();
				//ma_video()
				
				   // document.write("<script src='../../../js/mediaelement-and-player.js'><\/script>"); 
				//aler("12312")
				instance.close();
			},
		});
	};



	// Add a button that opens a window
	editor.ui.registry.addButton('example', {
		icon: 'image',
		onAction: function() {
			window.addEventListener('message', function(event) {
				window.mon_message = event.data.data.mon_message;
				//alert(mon_message)
				//alert(JSON.stringify(mon_message))
				//editor.windowManager.alert(JSON.stringify(data));
				// Do something with the data received here
				//console.log('message received from TinyMCE', data);
			});
			
	
			// Open window
			openDialog();
		}
	});

	// Adds a menu item, which can then be included in any menu via the menu/menubar configuration
	editor.ui.registry.addMenuItem('example', {
		text: 'Example plugin',
		onAction: function() {
			// Open window
			openDialog();
		}
	});

	return {
		getMetadata: function() {
			return {
				name: "Example plugin",
				url: "http://exampleplugindocsurl.com"
			};
		}
	};
});
