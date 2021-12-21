import React, { Component } from "react";
import { render } from "react-dom";
import HomePage from "./Homepage";

export default class App extends Component {

  render() {
    return (
      <div>
        <HomePage/>
      </div>
    );
  }
}
const appDiv = document.getElementById("app");
console.log(">>>>>>>>>>",appDiv)

render(<App />, appDiv);