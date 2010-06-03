(function($) {
  //A simplification of http://tweet.seaofclouds.com/ for my personal site
  $.fn.tweet = function(o){
    var s = {
      username: ["keithentzeroth"],
      avatar_size: null,
      count: 3,
      loading_text: null,
    };
    
    if(o) $.extend(s, o);
    
    $.fn.extend({
      linkUrl: function() {
        var returning = [];
        var regexp = /((ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?)/gi;
        this.each(function() {
          returning.push(this.replace(regexp,"<a href=\"$1\">$1</a>"));
        });
        return $(returning);
      },
      linkUser: function() {
        var returning = [];
        var regexp = /[\@]+([A-Za-z0-9-_]+)/gi;
        this.each(function() {
          returning.push(this.replace(regexp,"<a href=\"http://twitter.com/$1\">@$1</a>"));
        });
        return $(returning);
      },
      linkHash: function() {
        var returning = [];
        var regexp = /(?:^| )[\#]+([A-Za-z0-9-_]+)/gi;
        this.each(function() {
          returning.push(this.replace(regexp, ' <a href="http://search.twitter.com/search?q=&tag=$1&lang=all&from='+s.username.join("%2BOR%2B")+'">#$1</a>'));
        });
        return $(returning);
      },
      capAwesome: function() {
        var returning = [];
        this.each(function() {
          returning.push(this.replace(/\b(awesome)\b/gi, '<span class="awesome">$1</span>'));
        });
        return $(returning);
      },
      capEpic: function() {
        var returning = [];
        this.each(function() {
          returning.push(this.replace(/\b(epic)\b/gi, '<span class="epic">$1</span>'));
        });
        return $(returning);
      },
      makeHeart: function() {
        var returning = [];
        this.each(function() {
          returning.push(this.replace(/(&lt;)+[3]/gi, "<tt class='heart'>&#x2665;</tt>"));
        });
        return $(returning);
      }
    });

    function parse_date(date_str) {
      // The non-search twitter APIs return inconsistently-formatted dates, which Date.parse
      // cannot handle in IE. We therefore perform the following transformation:
      // "Wed Apr 29 08:53:31 +0000 2009" => "Wed, Apr 29 2009 08:53:31 +0000"
      return Date.parse(date_str.replace(/^([a-z]{3})( [a-z]{3} \d\d?)(.*)( \d{4})$/i, '$1,$2$4$3'));
    }

    function relative_time(time_value) {
      var parsed_date = parse_date(time_value);
      var relative_to = (arguments.length > 1) ? arguments[1] : new Date();
      var delta = parseInt((relative_to.getTime() - parsed_date) / 1000);
      var pluralize = function (singular, n) {
        return '' + n + ' ' + singular + (n == 1 ? '' : 's');
      };
      if(delta < 60) {
      return 'less than a minute ago';
      } else if(delta < (60*60)) {
      return 'about ' + pluralize("minute", parseInt(delta / 60)) + ' ago';
      } else if(delta < (24*60*60)) {
      return 'about ' + pluralize("hour", parseInt(delta / 3600)) + ' ago';
      } else {
      return 'about ' + pluralize("day", parseInt(delta / 86400)) + ' ago';
      }
    }

    function build_url() {
      var proto = ('https:' == document.location.protocol ? 'https:' : 'http:');
      if (s.list) {
        return proto+"//api.twitter.com/1/"+s.username[0]+"/lists/"+s.list+"/statuses.json?per_page="+s.count+"&callback=?";
      } else if (s.query == null && s.username.length == 1) {
        return proto+'//api.twitter.com/1/statuses/user_timeline.json?screen_name='+s.username[0]+'&count='+s.count+'&callback=?';
      } else {
        var query = (s.query || 'from:'+s.username.join(' OR from:'));
        return proto+'//search.twitter.com/search.json?&q='+escape(query)+'&rpp='+s.count+'&callback=?';
      }
    }

    return this.each(function(i, widget){

      var loading = $('<p class="loading">'+s.loading_text+'</p>');

      if(typeof(s.username) == "string"){
        s.username = [s.username];
      }

      if (s.loading_text) $(widget).append(loading);
      $.getJSON(build_url(), function(data){
        if (s.loading_text) loading.remove();
        var tweets = (data.results || data);        
        var avatar;
        var list = $('<ul class="tweet_list">').appendTo(widget);

        $.each(tweets, function(i,item){
          var from_user = item.from_user || item.user.screen_name;
          var profile_image_url = item.profile_image_url || item.user.profile_image_url;
          var avatar_template = '<p class="avatar"><a class="tweet_avatar" href="http://twitter.com/'+from_user+'"><img src="'+profile_image_url+'" height="'+s.avatar_size+'" width="'+s.avatar_size+'" alt="'+from_user+'\'s avatar" title="'+from_user+'\'s avatar" border="0"/></a><a class="user" href="http://twitter.com/'+from_user+'" title="View '+from_user+' on Twitter">@'+from_user+'</a></p>';
          avatar = (s.avatar_size ? avatar_template : '');

          var date = '<small class="tweet_time"><a href="http://twitter.com/'+from_user+'/statuses/'+item.id+'" title="view tweet on twitter">'+relative_time(item.created_at)+'</a></small>';
          var text = '<span class="tweet_text">' +$([item.text]).linkUrl().linkUser().linkHash().makeHeart().capAwesome().capEpic()[0]+ '</span>';

          // until we create a template option, arrange the items below to alter a tweet's display.
          list.append('<li>' +  text + date  +'</li>');

          list.children('li:first').addClass('tweet_first');
          list.children('li:odd').addClass('tweet_even');
          list.children('li:even').addClass('tweet_odd');
        });
        $(widget).prepend(avatar);
        $(widget).trigger("loaded").trigger((tweets.length == 0 ? "empty" : "full"));
      });

    });
  };
})(jQuery);    