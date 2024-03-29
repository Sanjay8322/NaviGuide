class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
            recButton: document.querySelector('.rec__button'),

        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const {openButton, chatBox, sendButton, recButton} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox)) 

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        recButton.addEventListener('click', () => this.onRecButton(chatBox))


        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })


    }

    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box
        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSendButton(chatbox) {
        let textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);

        fetch('/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(r => r.json())
          .then(r => {
            let msg2 = { name: "Sam", message: r.answer };
            this.messages.push(msg2);
            this.updateChatText(chatbox)
            textField.value = ''

            console.log(r.audio_path)
            
            var audio_url = '/get-audio?audio_path=' + r.audio_path
            fetch(audio_url)
            .then(handleAudioResponse)
            .catch(error => console.error(error));

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
          });
    }

    updateChatText(chatbox) {
        let html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "Sam")
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }


    onRecButton(chatbox) {
        console.log(chatbox);
        fetch('/get_recommendations?user_id=1', {
            method: 'GET',
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(r => r.json())
          .then(recommendations => {
              console.log(recommendations)
            let msg = { name: "Sam", message: "Recommendations for you: " + recommendations['recommendations'].join(", ") };
            this.messages.push(msg);
            this.updateChatText(chatbox);
        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox);
          });
    }

}


const chatbox = new Chatbox();
chatbox.display();


async function handleAudioResponse(response) {
    // Handle audio file
    if (response.headers.get('content-type').startsWith('audio')) {
      const audioBlob = await response.blob();
      const audioURL = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioURL);
      audio.play();
    }
  
    // Handle JSON response
    const data = await response.json();
    console.log(data);
    // Do something with the JSON data
  }

