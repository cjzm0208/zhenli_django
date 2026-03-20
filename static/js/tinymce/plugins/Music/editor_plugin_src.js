/**
 * $RCSfile: editor_plugin_src.js,v $
 * $Revision: 1.34 $
 * $Date: 5:45 AM 4/8/2006 $
 *
 * @author Wuvist
 * @copyright Copyright © 2004-2006, Wuvist, All rights reserved.
 */

/* Import plugin specific language pack */
tinyMCE.importPluginLanguagePack('Music', 'en,tr,de,sv,zh_cn,cs,fa,fr_ca,fr,pl,pt_br,nl,da,he,nb,hu,ru,ru_KOI8-R,ru_UTF-8,nn,es,cy,is,zh_tw,zh_tw_utf8,sk,pt_br');

var TinyMCE_MusicPlugin = {
	getInfo : function() {
		return {
			longname : 'Music',
			author : 'Wuvist',
			authorurl : 'http://www.blogwind.com/Wuvist',
			infourl : 'http://www.blogwind.com/Wuvist',
			version : tinyMCE.majorVersion + "." + tinyMCE.minorVersion
		};
	},

	initInstance : function(inst) {
		if (!tinyMCE.settings['Music_skip_plugin_css'])
			tinyMCE.importCSS(inst.getDoc(), tinyMCE.baseURL + "/plugins/Music/css/content.css");
	},

	getControlHTML : function(cn) {
		switch (cn) {
			case "Music":
				return tinyMCE.getButtonHTML(cn, 'lang_Music_desc', '{$pluginurl}/images/Music.gif', 'mceMusic');
		}

		return "";
	},

	execCommand : function(editor_id, element, command, user_interface, value) {
		// Handle commands
		switch (command) {
			case "mceMusic":
				var name = "", swffile = "", swfwidth = "", swfheight = "", action = "insert";
				var template = new Array();
				var inst = tinyMCE.getInstanceById(editor_id);
				var focusElm = inst.getFocusElement();

				template['file']   = '../../plugins/Music/Music.htm'; // Relative to theme
				template['width']  = 430;
				template['height'] = 175;

				template['width'] += tinyMCE.getLang('lang_Music_delta_width', 0);
				template['height'] += tinyMCE.getLang('lang_Music_delta_height', 0);

				// Is selection a image
				if (focusElm != null && focusElm.nodeName.toLowerCase() == "img") {
					name = tinyMCE.getAttrib(focusElm, 'class');

					if (name.indexOf('mceItemMusic') == -1) // Not a Music
						return true;

					// Get rest of Music items
					swffile = tinyMCE.getAttrib(focusElm, 'alt');

					if (tinyMCE.getParam('convert_urls'))
						swffile = eval(tinyMCE.settings['urlconverter_callback'] + "(swffile, null, true);");

					swfwidth = tinyMCE.getAttrib(focusElm, 'width');
					swfheight = tinyMCE.getAttrib(focusElm, 'height');
					action = "update";
				}

				tinyMCE.openWindow(template, {editor_id : editor_id, inline : "yes", swffile : swffile, swfwidth : swfwidth, swfheight : swfheight, action : action});
			return true;
	   }

	   // Pass to next handler in chain
	   return false;
	},

	cleanup : function(type, content) {
		switch (type) {
			case "insert_to_editor_dom":
				// Force relative/absolute
				if (tinyMCE.getParam('convert_urls')) {
					var imgs = content.getElementsByTagName("img");
					for (var i=0; i<imgs.length; i++) {
						if (tinyMCE.getAttrib(imgs[i], "class") == "mceItemMusic") {
							var src = tinyMCE.getAttrib(imgs[i], "alt");

							if (tinyMCE.getParam('convert_urls'))
								src = eval(tinyMCE.settings['urlconverter_callback'] + "(src, null, true);");

							imgs[i].setAttribute('alt', src);
							imgs[i].setAttribute('title', src);
						}
					}
				}
				break;

			case "get_from_editor_dom":
				var imgs = content.getElementsByTagName("img");
				for (var i=0; i<imgs.length; i++) {
					if (tinyMCE.getAttrib(imgs[i], "class") == "mceItemMusic") {
						var src = tinyMCE.getAttrib(imgs[i], "alt");

						if (tinyMCE.getParam('convert_urls'))
							src = eval(tinyMCE.settings['urlconverter_callback'] + "(src, null, true);");

						imgs[i].setAttribute('alt', src);
						imgs[i].setAttribute('title', src);
					}
				}
				break;

			case "insert_to_editor":
				var startPos = -1;
				var embedList = new Array();

				// Fix the object elements
				content = content.replace(new RegExp('<[ ]*object','gi'),'<object');
				content = content.replace(new RegExp('<[ ]*/object[ ]*>','gi'),'</object>');
				// Parse all object tags
				while ((startPos = content.indexOf('<object type="application/x-mplayer2"', startPos+1)) != -1) {
					var endPos = content.indexOf('>', startPos);
					var attribs = TinyMCE_MusicPlugin._parseAttributes(content.substring(startPos + 7, endPos));
					embedList[embedList.length] = attribs;
				}


				// Parse all object tags and replace them with images from the embed data
				var index = 0;

				while ((startPos = content.indexOf('<object type="application/x-mplayer2"', startPos)) != -1) {
					if (index >= embedList.length)
						break;

					var attribs = embedList[index];

					// Find end of object
					endPos = content.indexOf('</object>', startPos);
					endPos += 9;

					// Insert image
					var contentAfter = content.substring(endPos);
					
					content = content.substring(0, startPos);
					content += '<img width="' + attribs["width"] + '" height="' + attribs["height"] + '"';
					content += ' src="' + (tinyMCE.getParam("theme_href") + '/images/spacer.gif') + '" title="' + attribs["data"] + '"';
					content += ' alt="' + attribs["data"] + '" class="mceItemMusic" />' + content.substring(endPos);
					content += contentAfter;
					index++;

					startPos++;
				}

				break;

			case "get_from_editor":
				// Parse all img tags and replace them with object+embed
				var startPos = -1;

				while ((startPos = content.indexOf('<img', startPos+1)) != -1) {
					var endPos = content.indexOf('/>', startPos);
					var attribs = TinyMCE_MusicPlugin._parseAttributes(content.substring(startPos + 4, endPos));

					// Is not Music, skip it
					if (attribs['class'] != "mceItemMusic")
						continue;

					endPos += 2;

					var embedHTML = '';

					// Insert object + embed
					embedHTML += '<object type="application/x-mplayer2" data="';
					embedHTML += attribs["title"] + '"';
					embedHTML += ' width="' + attribs["width"] + '" height="' + attribs["height"] + '">';
					embedHTML += '<param name="src" value="' + attribs["title"] + '" />';
					embedHTML += '<param name="filename" value="' + attribs["title"] + '" />';
					embedHTML += '<param name="type" value="application/x-mplayer2" />';
					embedHTML += '<param name="AutoStart" value="0" />';
					embedHTML += '</object>';

					// Insert embed/object chunk
					chunkBefore = content.substring(0, startPos);
					chunkAfter = content.substring(endPos);
					content = chunkBefore + embedHTML + chunkAfter;
				}
				break;
		}

		// Pass through to next handler in chain
		return content;
	},

	handleNodeChange : function(editor_id, node, undo_index, undo_levels, visual_aid, any_selection) {
		if (node == null)
			return;

		do {
			if (node.nodeName == "IMG" && tinyMCE.getAttrib(node, 'class').indexOf('mceItemMusic') == 0) {
				tinyMCE.switchClass(editor_id + '_Music', 'mceButtonSelected');
				return true;
			}
		} while ((node = node.parentNode));

		tinyMCE.switchClass(editor_id + '_Music', 'mceButtonNormal');

		return true;
	},

	// Private plugin internal functions

	_parseAttributes : function(attribute_string) {
		var attributeName = "";
		var attributeValue = "";
		var withInName;
		var withInValue;
		var attributes = new Array();
		var whiteSpaceRegExp = new RegExp('^[ \n\r\t]+', 'g');

		if (attribute_string == null || attribute_string.length < 2)
			return null;

		withInName = withInValue = false;

		for (var i=0; i<attribute_string.length; i++) {
			var chr = attribute_string.charAt(i);

			if ((chr == '"' || chr == "'") && !withInValue)
				withInValue = true;
			else if ((chr == '"' || chr == "'") && withInValue) {
				withInValue = false;

				var pos = attributeName.lastIndexOf(' ');
				if (pos != -1)
					attributeName = attributeName.substring(pos+1);

				attributes[attributeName.toLowerCase()] = attributeValue.substring(1);

				attributeName = "";
				attributeValue = "";
			} else if (!whiteSpaceRegExp.test(chr) && !withInName && !withInValue)
				withInName = true;

			if (chr == '=' && withInName)
				withInName = false;

			if (withInName)
				attributeName += chr;

			if (withInValue)
				attributeValue += chr;
		}

		return attributes;
	}
};

tinyMCE.addPlugin("Music", TinyMCE_MusicPlugin);
