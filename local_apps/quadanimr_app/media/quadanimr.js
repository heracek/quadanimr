function animate_image(animation_div) {
    var background_positions = animation_div.css('background-position').split(' ');
    
    var x = -Number(background_positions[0].slice(0, -2))
    var y = -Number(background_positions[1].slice(0, -2))
    
    if (x >= 900) {
        x = 0;
        y += 400;
    } else {
        x += 300;
    }
    
    if (y >= 800) {
        y = 0;
    }
    
    animation_div.css('background-position', -x + 'px ' + -y + 'px');
}

function animate_thumb(animation_div) {
    var i = animation_div[0].i
    if (i === undefined) {
        i = animation_div[0].i = 0
    }
    
    ++i;
    if (i > 7) { i = 0;}
    
    animation_div[0].i = i;
    xy = [[0, 8], [45, 8], [90, 8], [135, 8], [0, 68], [45, 68], [90, 68], [135, 68]][i]
    
    var x = xy[0];
    var y = -xy[1];
    
    animation_div.css('background-position', x + 'px ' + y + 'px');
}

function reset_animate_thumb(animation_div) {
    animation_div[0].i = -1;
    animate_thumb(animation_div);
}

function setTimerTo(time) {
    $(document).stopTime("animationTimer");
    
    $(document).everyTime(time, "animationTimer", function() {
        animate_image($("#animation"));
    });
}

function stopThumbAnim() {
    $(document).stopTime("thumbAnimationTimer");
}

function startThumbAnim(frame_time, thumb) {
    $(document).everyTime(frame_time, "thumbAnimationTimer", function() {
        animate_thumb(thumb);
    });
}


$(document).ready(function() {
    if ($("#animation").length != 0) {
        setTimerTo(150);
    }
    
    $(".animation-thumb").hover(
        function () {
            startThumbAnim(150, $(this));
        }, 
        function () {
            reset_animate_thumb($(this))
            stopThumbAnim();
        }
    );
});