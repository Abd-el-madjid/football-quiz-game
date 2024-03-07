var divs = $('.show-section section');
var now = 0; // currently shown div
divs.hide().first().show(); // hide all divs except the first

// show active step
function showActiveStep() {
    $(".step-bar .bar .fill").eq(now).addClass('w-100');
}

// function to show next step
function showNextStep() {
    // Check if there is a selected option in the current step
    var currentStepInputs = $(`#step${now + 1} input[name="op${now + 1}"]:checked`);

    if (currentStepInputs.length === 0) {
        // No option selected, display an error message
        (function (el) {
            setTimeout(function () {
                el.children().remove('.reveal');
            }, 3000);
        }($('#error').append('<div class="reveal alert alert-danger">Choose an option!</div>')));

        return;
    }

    divs.eq(now).hide();

    // Check if the current step is the last step
    if (now + 1 < divs.length) {
        now = now + 1;
        divs.eq(now).show(); // show next
        showActiveStep();
    } else {
        // Last step, call showresult function
        showresult();
    }
}

// function to show previous step
function showPreviousStep() {
    $('.radio-field').addClass('bounce-left');
    $('.radio-field').removeClass('bounce-right');
    $(".step-bar .bar .fill").eq(now).removeClass('w-100');
    divs.eq(now).hide();
    now = (now > 0) ? now - 1 : divs.length - 1;
    divs.eq(now).show(); // show previous
    showActiveStep();
}

// handle next button click
$(".next").on('click', function () {
    showNextStep();
});

// handle previous button click
$(".prev").on('click', function () {
    showPreviousStep();
});

// quiz validation
var checkedradio = false;

// form validation
$(document).ready(function () {


         $('#reload_game').on('click', function () {
             // Reload the page
             console.log("relaod game clicked")
             location.reload();
         });
    
    
    $(".next-btn").on('click', function () {
        radiovalidate(now + 1);

        if (!checkedradio) {
            // No option selected, display an error message
            (function (el) {
                setTimeout(function () {
                    el.children().remove('.reveal');
                }, 3000);
            }($('#error').append('<div class="reveal alert alert-danger">Choose an option!</div>')));

            radiovalidate(now + 1);
            return;
        }

        $(`.radio-field`).removeClass('bounce-left');
        $(`.radio-field`).addClass('bounce-right');
        setTimeout(function () {
            showNextStep();
        }, 900);
        countresult(now + 1);
    });


    // handle last step button click
    $("#sub").on('click', function () {
        radiovalidate(now + 1);

        if (!checkedradio) {
            // No option selected, display an error message
            (function (el) {
                setTimeout(function () {
                    el.children().remove('.reveal');
                }, 3000);
            }($('#error').append('<div class="reveal alert alert-danger">Choose an option!</div>')));

            radiovalidate(now + 1);
            return;
        }

        countresult(now + 1);

        // Check if the current step is the last step
        if (now + 1 === divs.length) {
            showresult();
        }
    });
});
