import React from 'react';
import axios from 'axios';
import './index.css'
class App extends React.Component {
  constructor() {
    super();
    this.state = {
      image: null,
      loading: false,
      status: null,
    }
    this.onChangeHandeler = this.onChangeHandeler.bind(this);
    this.onClickHandeler = this.onClickHandeler.bind(this)
  }

  onChangeHandeler(e) {
    this.setState({ [e.target.name]: e.target.files[0] })
    // console.log(e.target.files[0])
  }

  onClickHandeler() {
    this.setState({ loading: true, status: null })
    const data = new FormData()
    data.append('file', this.state.image);
    const config = {
      headers: {
        'content-type': 'multipart/form-data'
      }
    };
    axios.post("http://localhost:5000/upload", data, config)
      .then(res => {
        this.setState({ loading: false, status: res.data.status === '1' ? 'NEGATIVE' :'POSITIVE'})
        console.log(res.data)
      })
      .catch(err => {
        console.log(err)
      })
  }

  render() {
    return (
      <div className="container">
        <div>
          <h2 style={{ color: "rgb(219, 19, 19)" }}>Upload your X-Ray to check for COVID-19</h2>
        </div>
        <div className="input-cont">
          <label style={{ color: "white" }}>
            <div style={{ padding: "10px" }}> Click to Upload file </div>
            <input type="file" id="fileInput" name="image" onChange={this.onChangeHandeler} />
          </label>
        </div>
        <div>
          <button type="button" id="button" onClick={this.onClickHandeler}>Upload</button>
        </div >
        {this.state.loading === false && this.state.status === null ?
          <div className="output">
            <p className="ptext">Result</p>
            <p className="rtext">No Photo To Analyse</p>
          </div>
          :
          <div className="output">
            <p className="ptext">Result</p>
            <p className="ptext">{this.state.loading === true ? "Wait... Analysing" : ""}</p>
            {this.state.status !== null && this.state.status === "POSITIVE"
              ? <p className="rtext"> {this.state.status}</p>
              : <p className="gtext"> {this.state.status}</p>
            }
          </div>
        }
      </div>
    )
  }
}

export default App;
