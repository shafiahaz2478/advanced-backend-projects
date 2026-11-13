import {useState} from "react";
import {Navigate} from "react-router";

function Login({login,authed}){
      const [username, setUsername] = useState("");
      const [password, setPassword] = useState("");

      function handleUser(e) {    // function is an event handler used to update the component's state whenever someone types into the input field
         setUsername(e.target.value);

      }
      function handlePass(e) {    // function is an event handler used to update the component's state whenever someone types into the input field
         setPassword(e.target.value);

      }
      function handleSubmit(e) {
        e.preventDefault(); // Prevents the page from refreshing on form submit
         // Pass the current RollNo state up to the parent component
        login(username,password);


      }
      if (authed === true){
          return <Navigate replace to="/" />;
      }
    return (

        <form className="inline-form" onSubmit={handleSubmit}>
          <label className="field">Enter your Username:
            <input
              type="text"
              value={username}
              onChange={handleUser}
            />
          </label>
            <label className="field">Enter your password:
            <input
              type="password"
              value={password}
              onChange={handlePass}
            />
          </label>
          <button type='submit'>Login</button>
        </form>
    )

}


export default Login