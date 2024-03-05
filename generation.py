from openai import OpenAI
from dotenv import load_dotenv
import os
from word_count import system_message

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_documentation",
            "description": "Gets the documentation for a given component",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the component",
                    }
                },
                "required": ["name"],
            },
        }
    }
]

GPT_MODEL = "gpt-4-turbo-preview"

messages = []
messages.append({"role": "system", "content": "You are a professional web developer using the Reflex Python framework to develop a web app. Take a user description"})
messages.append({"role": "system", "content": system_message})
messages.append({"role": "user", "content": "A single sign in page. Nothing more, just the sign in component, a user model, and state to manage the signed in user."})

def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools, # type: ignore
            tool_choice=tool_choice, # type: ignore
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e
    
def design_app_from_description():
    pass
    
response = chat_completion_request(messages, tools=tools)

# phase 1: app description -> detailed description
# consists of 
# phase 2: high level component descriptions + reflex docs + plugin descriptions -> select components + plugins
# phase >3: selected components' descriptions, api_ref, examples + reflex docs + selected plugin docs -> written page

'''To implement a simple sign-in page with Reflex, we will create a basic user model, state to manage the signed-in user, and the sign-in component itself. Here's how the structure will look in a single file:

```python
# Import necessary packages
import reflex as rx

# Define the User model (typically, you would interact with a database)
class User(rx.Model, table=True):
    username: rx.Var[str]
    password: rx.Var[str]  # In a real application, passwords should be hashed

# State to manage the signed-in user
class AuthState(rx.State):
    current_user: rx.Var[User] = None
    auth_message: rx.Var[str] = ""

    def sign_in(self, username: str, password: str):
        # In a real application, verify the user credentials against a database
        # This is a simplified simulation of such a process
        if username == "admin" and password == "secret":
            self.current_user = User(username=username, password=password)
            self.auth_message = "Sign in successful!"
        else:
            self.auth_message = "Invalid username or password."

# Sign-in form component
@rx.page(route="/sign-in")
def sign_in_page():
    def handle_submit(form_data: dict):
        username = form_data["username"]
        password = form_data["password"]
        AuthState.sign_in(username, password)

    return rx.fragment(
        rx.form(
            rx.vstack(
                rx.text("Sign in"),
                rx.input(id="username", placeholder="Username"),
                rx.input(id="password", placeholder="Password", type="password"),
                rx.button(content="Sign In"),
            ),
            on_submit=handle_submit,
        ),
        # Display authentication message
        rx.cond(
            AuthState.auth_message != "",
            rx.text(AuthState.auth_message),
        ),
    )

# Define the app and add sign-in page to it
app = rx.App()
app.add_page(sign_in_page)
```

**Important Notes:**
1. **Password Storage**: In this example, we simply compare a plain password, which is not secure. In real applications, passwords should be salted and hashed before being stored. Use established libraries for handling user authentication securely.
2. **Data Storage**: The `User` model in this example doesn't interact with a database. For persistent user data, you would integrate Reflex with a database and replace the auth check with a query to validate the credentials.
3. **Client-side Validation**: For simplicity, client-side validation (i.e., ensuring that usernames and passwords meet certain constraints before submission) is not performed. Implementing such validation can improve the user experience.

This example covers just one aspect of user authentication. A complete system would also need registration, password hashing, sessions, and more.'''