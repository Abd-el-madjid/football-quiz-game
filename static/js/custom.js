









document.getElementById("navbarDropdown").addEventListener('click', function () {
    // Toggle the "non" class for both divs
    var dropdownMenu = document.querySelector(".dropdown-menu");
    dropdownMenu.classList.toggle("non");
});













var divs = $('.show-section section');
var now = 0; // currently shown div
divs.hide().first().show(); // hide all divs except the first

// show active step
function showActiveStep() {
    console.log('Showing active step:', now + 1);
    $(".step-bar .bar .fill").eq(now).addClass('w-100');
}

// function to show next step
// function to show next step
function showNextStep() {
    // Check if there is a selected option in the current step
    var currentStepInputs = divs.eq(now).find('input:checked');

    if (currentStepInputs.length === 0) {
        // No option selected, display an error message
        console.log('No option selected in current step:', now + 1);
        displayErrorMessage('Choose an option!');
        return;
    } else {
        checkedradio = true; // Update the checkedradio variable
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
    console.log('Next button clicked');
    showNextStep();
});

// handle previous button click
$(".prev").on('click', function () {
    console.log('Previous button clicked');
    showPreviousStep();
});

// quiz validation
var checkedradio = false;

// form validation
$(document).ready(function () {
    console.log("load game");



$("#quiz-form").submit(function (e) {
    e.preventDefault();  // Prevent the default form submission

    // Get the form action URL from the form's action attribute
    var formUrl = $(this).attr("action");

    // Get the form data
    var formData = $(this).serialize();

    // Submit the form asynchronously using AJAX
    $.ajax({
        type: "POST",
        url: formUrl,
        data: formData,
        success: function (response) {
            console.log('AJAX request successful:', response);

            // Display the score information
            $(".u_score_point").html(response.result_message + " Point");
            $(".u_prcnt").html(response.result_message + " %");

            // Iterate through the result_data array in the response
            var existingDetailsSection = $("#details-section");
$.each(response.result_data, function (index, result) {
    // Create the details section div
    

    // Create the heading for the details section
   

    // Create the list for question details
    var list = $('<ul class="list-group"></ul>');

    // Create and append the question text
    var questionItem = $('<li class="list-group-item questionText">Question: ' + result.question + '</li>');
    list.append(questionItem);

    // Create and append the correct answer details
    var correctAnswerItem = $('<li class="list-group-item correctAnswer"><span class="material-symbols-outlined">done</span> <span class="letter correct_letter">' + result.correct_answer_letter + '</span> Correct Answer: ' + result.correct_answer_value + '</li>');
    list.append(correctAnswerItem);

    // Check if the answer is incorrect
    if (result.chosen_answer_letter != result.correct_answer_letter) {
        // If incorrect, create and append the chosen answer details
        var chosenAnswerItem = $('<li class="list-group-item chosenAnswer"><span class="material-symbols-outlined">close</span> <span class="letter chosen_letter">' + result.chosen_answer_letter + '</span> Chosen Answer: ' + result.user_answer_value + '</li>');
        list.append(chosenAnswerItem);
    }
    else if(result.chosen_answer_letter == result.correct_answer_letter) {
         var chosenAnswerItem = $('<li class="list-group-item correctAnswer"><span class="material-symbols-outlined">done</span> <span class="letter correct_letter">' + result.chosen_answer_letter + '</span> Chosen Answer: ' + result.user_answer_value + '</li>');
     list.append(chosenAnswerItem);
    }

    // Append the list to the details section
    existingDetailsSection.append(list);

});

        },
        error: function (error) {
            console.error("Error submitting the form:", error);
        }
    });
});


    $("#show_result").on('click', function () {
        // Toggle the "non" class for both divs
        $("#details-container").toggleClass("non");
        $("#details-section").toggleClass("non");
    });

    $("#navbarDropdown").on('click', function () {
        // Toggle the "non" class for both divs
        $(".dropdown-menu").toggleClass("non");
    });

    $('.reload_game').on('click', function () {
        // Reload the page
        console.log("Reload game clicked");
        location.reload();
    });

    $(".next-btn").on('click', function () {
        console.log('Next button clicked in the last section');
        radiovalidate(now + 1);

        if (!checkedradio) {
            // No option selected, display an error message
            console.error('No option selected in the last section');
            displayErrorMessage('Choose an option!');
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
        console.log('Submit button clicked');
        radiovalidate(now + 1);

        if (!checkedradio) {
            // No option selected, display an error message
            console.error('No option selected on Submit button click');
            displayErrorMessage('Choose an option!');
            return;
        }

        countresult(now + 1);

        // Check if the current step is the last step
        if (now + 1 === divs.length) {
            showresult();
        }
    });
});

// Function to display an error message
function displayErrorMessage(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'custom-alert alert-error';
    alertDiv.innerHTML = '<div class="icon__wrapper"><span class="material-symbols-outlined">error</span></div><p>' + message + '</p>';

    const body = document.getElementById('body');
    document.body.appendChild(alertDiv);
    setTimeout(function () {
        alertDiv.remove();
    }, 3000);
}
