/**
 * Created by rockstar645 on 11/13/16.
 */
$(function(){

    $.ajax({
        get:"{% url 'scrape' %}",
        success:function(data){
            $('#token').text(data)
        }
        }
    )
});