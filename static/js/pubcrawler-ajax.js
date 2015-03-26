$(document).ready(function(){

	$('#like').click(function(){
		var crawlid;
		crawlid = $(this).attr("data-crawlid");
		$.get('/pubcrawl/rate_crawl/', {crawl_id: crawlid}, function(data){
				   $('#score').html(data);
				   $('#like').hide();
		});
	});
	
	$('ul.nav.nav-pills li').click(function(){
        var sortby;
        sortby = $(this).attr("data-sorttype");
        var crawl = $(".hiddenCrawls");
        var crawls = [];
        for (i=0; i < crawl.length; i++ ) {
            crawls.push(crawl[i].innerHTML.toString());
        }
        $.get('/pubcrawl/crawl_list/', {sort_by: sortby, crawls: crawls}, function(data){
            $('#content').html(data);
        });
		
        $('ul.nav-pills li.active').removeClass('active');
        $(this).addClass('active');
    });
	
	$('#prev, #next').click(function(){
	    var sortby;
		sortby = $('ul.nav-pills li.active').attr("data-sorttype");
		var startat;
		startat = $('#current_page').value();
		startat = parseInt(startat) + parseInt($(this).value());
		
		$.get('/pubcrawl/crawl_list/', {sort_by: sortby}, function(data){
            $('#content').html(data);
        });
	});
});