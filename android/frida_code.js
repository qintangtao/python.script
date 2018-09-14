send(11111);
if(Java.available) {
	send("Java.available is True");
	Java.perform(function(){
		var vi = Java.use("com.youku.upsplayer.module.VideoInfo");
		if (vi != undefined) {
			send("VideoInfo: " + vi.toString());
			vi.getAd.overload().implementation = function(){
				send("VideoInfo: getAd return null");
				return null;
			};
		} else {
			send("VideoInfo: undefined");
		};
	});
};
send(2222222);