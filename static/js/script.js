$(document).ready(function () {
  $(".submit-form").validate({
    rules: {
      username: {
        required: true,
        minlength: 4,
      },
      first_name: {
        required: true,
      },
      last_name: {
        required: true,
      },
      email: {
        required: true,
        email: true,
      },
      gender: {
        required: true,
      },
      phone_number: {
        required: true,
        digits: true,
        length: 10,
      },
      pass: {
        required: true,
        minlength: 8,
      },
      pass1: {
        required: true,
        minlength: 8,
      },
      house_name: {
        required: true,
      },
      street_name: {
        required: true,
      },
      city: {
        required: true,
      },
      post_code: {
        required: true,
        digits: true,
        minlength: true,
      },
    },
  
    messages: {
      username: {
        required: "Please enter your username",
      },
      first_name: {
        required: "Please enter your first_name",
      },
      last_name: {
        required: "Please enter your last_name",
      },
      email: {
        required: "Please enter a valid email",
      },
      gender: {
        required: "Please select gender",
      },
      phone_number: {
        required: "Please enter a valid phone number",
      },
      pass: {
        required: "Please enter your password",
      },
      house_name: {
        required: "Please enter your house name",
      },
      street_name: {
        required: "Please enter your street name",
      },
      city: {
        required: "Please enter your city",
      },
      post_code: {
        required: "Please enter your post code",
      },
    },
  });
});
