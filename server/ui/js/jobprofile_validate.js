$(document).ready(function () {
  $("#target").validate({
    rules: {

      code: {
        required: true,
        minlength: 5
      },
      desc: {
        required: true,
      },
      positions: {
        required: true,
        number: true,
        min: 1
      },
      edu: {
        required: true,
      },
      client: {
        required: true,
        minlength: 2
      },
      interview_pattern: {
        required: true
      },
      title: {
        required: true,
        minlength: 5
      },
      required_skills: {
        required: true
      },
      minexp: {
        required: true,
        number: true,
        min: 1
      },
      maxexp: {
        required: true,
        number: true,
        min: 1
      },
      functional_org: {
        required: true
      },
      location: {
        required: true,
      },
      jd: {
        required: true,
      },
      hr_name: {
        required: true,
      },
      hr_phone: {
        required: true,
      },
      hr_email: {
        required: true,
      },
      end_date: {
        required: true,
      },
      emp_type:{
        required: true,
      }

    },
    messages: {
      code: {
        required: "Please enter the Job Code.",
        minlength: "Job Code should be at least 5 characters."
      },
      desc: {
        required: "Please, describe the job."
      },
      positions: {
        required: "Please, select the number of positions.",
        number: "The positions should be in numerical.",
        min: "Minimum number of positions should be 1."
      },
      edu: {
        required: "Please, select the Education Qualification."
      },
      client: {
        required: "Please enter the client name.",
        minlength: "Client name should be at least 5 characters."
      },
      interview_pattern: {
        required: "Please, select the interview pattern."
      },
      title: {
        required: "Please, enter the Job Title.",
        minlength: "Job Title should be at least 5 characters."
      },
      required_skills: {
        required: "Please, select the skill."
      },
      minexp: {
        required: " Please, select the Minimum Experience.",
        number: "Experience should be a number.",
        min: "Experience should be at minimum of 1."
      },
      maxexp: {
        required: "Please select the Maximum Experience.",
        number: "Experience should be a number.",
        min: "Experience should be at maximum of 35."
      },
      functional_org: {
        required: "Please, select the functional organisation."
      },
      location: {
        required: "Please, enter the location.",
        location: "Please enter the valid location.",
      },
      jd: {
        required: "Please, upload the Job Description file.",
      },
      emp_type: {
        required: "please, select employeement Type"
      },
      hr_name: {
        required: "Please, enter the HR Name.",
      },
      hr_phone: {
        required: "Please, enter the HR phone number.",
      },
      hr_email: {
        required: "Please, enter HR email address.",
      },
      end_date: {
        required: "Please, select the end date.",
      },
    }
  });
});