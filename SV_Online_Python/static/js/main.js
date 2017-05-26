$("body").click(function() {
    $("#right_menu").remove();
});

$(document).keydown(function(e) {
    if ((e.metaKey == true || e.ctrlKey == true) && e.keyCode == 83) {
        e.preventDefault();
        save_current();
        current_change = 0;
    }
});

var save_current = function() {
    $.ajax({
        type: "POST",
        url: "/update_file/",
        data: {
            'filename': current_file,
            'filecontent': editor.getValue()
        },
        dataType: "json",
        success: function(data) {
            humane.log("Saved: " + current_file);
        }
    });
};

var curr_right_click = "";
var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.getSession().setMode("ace/mode/c_cpp");
editor.$blockScrolling = Infinity;
document.getElementById('editor').style.fontSize = '14px';
var verify_button = function() {
    add_log("Verify: " + current_file);
    var perHeight = $($("#log_content").children()[0]).height();
    $("#log_content").scrollTop(perHeight * $("#log_content").children().length);
    $.ajax({
        type: "GET",
        url: "/verify/",
        data: {
            'filename': current_file
        },
        dataType: "json",
        success: function(data) {
            updateCT(data);
        }
    });
};

var updateCT = function(data) {
    add_log(data['term_out']);
    if (data['flag'] == 1) {
        humane.log("Verify Result: TRUE");
        add_log("[" + current_file + "]: True");
        zNodes2 = [];
        $.fn.zTree.init($("#tree2"), setting2, zNodes2);
    } else {
        humane.log("Verify Result: FALSE");
        add_log("[" + current_file + "]: False");
        line_array = data['data'];
        zNodes2 = [];
        zNodes2.push({
            id: 1,
            pId: 0,
            name: "Traces",
            'open': 'true'
        });
        i = 2;
        for (line_num in line_array) {
            zNodes2.push({
                id: i,
                pId: 1,
                name: "[LINE NO."+ line_array[line_num] +"] " + code_array[line_array[line_num] - 1].trim(),
                line_num: line_array[line_num],
            });
            i++;
        }
        $.fn.zTree.init($("#tree2"), setting2, zNodes2);
    }
    var perHeight = $($("#log_content").children()[0]).height();
    $("#log_content").scrollTop(perHeight * $("#log_content").children().length);
};

function get_filename(mnode) {
    if (mnode.level == 1) {
        return mnode.name;
    } else {
        result = mnode.name;
        var tempnode = mnode.getParentNode();
        while (tempnode.level > 0) {
            result = tempnode.name + "/" + result;
            tempnode = tempnode.getParentNode();
        }
        return result;
    }
}

$("#save_name").click(function(){
	var new_name = $("#new_name").val();
    if(!new_name.endsWith('.c')){
        humane.log("Raname Fails");
        $("#myModal").modal('hide');
        return;
    }
    $.ajax({
        type: "POST",
        url: "/api/rename_file/",
        data: {'new_name': new_name, 'filename': curr_right_click},
        dataType: "json",
        success: function(data) {
            if(data['status'] == 1){
                window.location.reload();
            }
            else{
                humane.log("Raname Fails");
                $("#myModal").modal('hide');
            }
        },
        error:function(data){
            humane.log("Raname Fails");
            $("#myModal").modal('hide');
        },
    });
});

$("#delete_file").click(function(){
    $.ajax({
        type: "POST",
        url: "/api/delete_file/",
        data: {'filename': curr_right_click},
        dataType: "json",
        success: function(data) {
            if(data['status'] == 1){
                window.location.reload();
            }
            else{
                humane.log("Delete Fails");
                $("#myModal2").modal('hide');
            }
        },
        error:function(data){
            humane.log("Delete Fails");
            $("#myModal2").modal('hide');
        },
    });
});

$("#save_folder_name").click(function(){
    var new_name = $("#rename_folder_name").val();
    $.ajax({
        type: "POST",
        url: "/api/rename_file/",
        data: {'new_name': new_name, 'filename': curr_right_click},
        dataType: "json",
        success: function(data) {
            if(data['status'] == 1){
                window.location.reload();
            }
            else{
                humane.log("Raname Fails");
                $("#myModal3").modal('hide');
            }
        },
        error:function(data){
            humane.log("Raname Fails");
            $("#myModal3").modal('hide');
        },
    });
});

$("#delete_folder").click(function(){
    $.ajax({
        type: "POST",
        url: "/api/delete_file/",
        data: {'filename': curr_right_click},
        dataType: "json",
        success: function(data) {
            if(data['status'] == 1){
                window.location.reload();
            }
            else{
                humane.log("Delete Fails");
                $("#myModal6").modal('hide');
            }
        },
        error:function(data){
            humane.log("Delete Fails");
            $("#myModal6").modal('hide');
        },
    });
});

$("#create_folder").click(function(){
    var new_name = $("#new_folder_name").val();
    $.ajax({
        type: "POST",
        url: "/api/create_folder/",
        data: {'filename': curr_right_click, 'new_name':new_name},
        dataType: "json",
        success: function(data) {
            if(data['status'] == 1){
                window.location.reload();
            }
            else{
                humane.log("Delete Fails");
                $("#myModal4").modal('hide');
            }
        },
        error:function(data){
            humane.log("Delete Fails");
            $("#myModal4").modal('hide');
        },
    });
});

$("#create_file").click(function(){
    var new_name = $("#new_file_name").val();
    if(!new_name.endsWith('.c')){
        humane.log("Create Fails");
        $("#myModal5").modal('hide');
        return;
    }
    $.ajax({
        type: "POST",
        url: "/api/create_file/",
        data: {'filename': curr_right_click, 'new_name':new_name},
        dataType: "json",
        success: function(data) {
            if(data['status'] == 1){
                window.location.reload();
            }
            else{
                humane.log("Delete Fails");
                $("#myModal5").modal('hide');
            }
        },
        error:function(data){
            humane.log("Delete Fails");
            $("#myModal5").modal('hide');
        },
    });
});

$("#folder-btn").click(function(){
   curr_right_click = ""; 
});

$("#file-btn").click(function(){
   curr_right_click = ""; 
});

var download_file = function(){
    window.location.href = '/download/?filename=' + curr_right_click +'&type=1';
}

var download_folder = function(){
    window.location.href = '/download/?filename=' + curr_right_click +'&type=2';
}

$("#ins1").click(function(){
    $("#ins1").fadeOut(500);
    $("#ins2").fadeIn(1000); 
});

$("#ins2").click(function(){
    $("#ins2").fadeOut(500);
    $("#ins3").fadeIn(1000); 
});

$("#ins3").click(function(){
    $("#ins3").fadeOut(500);
    $("#ins4").fadeIn(1000); 
});

$("#ins4").click(function(){
    $("#ins4").fadeOut(500);
});

var cia = [];

function arClick(that){
    cia = $(that).data('name').split(',');
    for(var i in cia)
        cia[i] = parseInt(cia[i]);
}

$("#btnAccept").click(function(){
    $.ajax({
        type: "GET",
        url: "/api/accept_common/",
        data: {'cia': cia.toString(),'filename':current_file},
        dataType: "json",
        success: function(data) {
            if(data['flag'] == 1)
                humane.log("Operation Succeeds");
        },
        error:function(data){
            humane.log("Operation Fails");
        },
    });
});

$("#btnReject").click(function(){
    $.ajax({
        type: "GET",
        url: "/api/reject_common/",
        data: {'cia': cia.toString(),'filename':current_file},
        dataType: "json",
        success: function(data) {
            if(data['flag'] == 1)
                humane.log("Operation Succeeds");
        },
        error:function(data){
            humane.log("Operation Fails");
        },
    });
});

