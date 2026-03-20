tinymce.PluginManager.add('emailtag', function(editor, url) {
	var openDialog = function() {
		tinymce.activeEditor.windowManager.openUrl({
			title: 'Tags d\'email',
			url: '/tinymc/emailtag/',
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
					text: 'Fermé'
				}
			],
			onAction: function(instance, trigger) {
				editor.insertContent(tag_email);
				instance.close();
			},
		});
	};



	// Add a button that opens a window
	editor.ui.registry.addButton('Emailtag', {
		icon: 'text-color',
		tooltip: 'Tags',
		onAction: function() {
			window.addEventListener('message', function(event) {
				window.tag_email = event.data.data.tag_email;
			});
			
	
			// Open window
			openDialog();
		}
	});

	// Adds a menu item, which can then be included in any menu via the menu/menubar configuration
	editor.ui.registry.addMenuItem('emailtag', {
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
