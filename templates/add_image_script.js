$(document).ready(function e(){
          $('button[id="upload"]')[0].disabled = true
          $('input[id="filename"]')[0].disabled = true
          $('#filename').tooltip('enable')
          });

          $('input[type="file"]').change(function e()
         {
          var filename = $('input[id="filename"]')[0]
          var isFile = $('input[type="file"]').length
          if (/^[0-9a-zA-Z\^\&\'\@\{\}\[\]\,\$\=\!\-\#\(\)\.\%\+\~\_]+$/.test(filename.value))
          {
          filename.classList.remove("is-valid")
          filename.classList.add("is-invalid")
          }
          else
          {
          filename.classList.remove("is-invalid")
          filename.classList.add("is-valid")
          }
          if (isFile == 1) {
            $('button[id="upload"]')[0].disabled = false
            $('input[id="filename"]')[0].disabled = false
          }
          else {
            $('button[id="upload"]')[0].disabled = true
          }}
          );

        $('input[id="filename"]').keyup(function e()
         {
          var filename = $('input[id="filename"]')[0]
          if (/^[0-9a-zA-Z\^\&\'\@\{\}\[\]\,\$\=\!\-\#\(\)\.\%\+\~\_]+$/.test(filename.value))
          {$('button[id="upload"]')[0].disabled = false
          filename.classList.remove("is-invalid")
          filename.classList.add("is-valid")
          }
          else
          {$('button[id="upload"]')[0].disabled = true
          filename.classList.remove("is-valid")
          filename.classList.add("is-invalid")}
          });

        $('input[type="file"]').change(function(e){
        var fileName = e.target.files[0].name;
        document.getElementById("filename").value = fileName
        document.getElementsByClassName("custom-file-label")[0].innerHTML = fileName;

        var filename = $('input[id="filename"]')[0]
          if (/^[0-9a-zA-Z\^\&\'\@\{\}\[\]\,\$\=\!\-\#\(\)\.\%\+\~\_]+$/.test(filename.value))
          {$('button[id="upload"]')[0].disabled = false
          filename.classList.remove("is-invalid")
          filename.classList.add("is-valid")
          }
          else
          {$('button[id="upload"]')[0].disabled = true
          filename.classList.remove("is-valid")
          filename.classList.add("is-invalid")}
            });