import './App.css';
import React from 'react';
import axios from 'axios';
import {Button} from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import Chart from 'chart.js/auto';

// BAR CHART!

class SentimentBarChart extends React.Component {
  constructor(props) {
    super(props);
    this.canvasRef = React.createRef();
  }

  componentDidMount() {
    this.myChart = new Chart(this.canvasRef.current, {
      type: 'bar',
      options: {
        maintainAspectRatio: true,
        scales: {
          yAxes: [
            {
              ticks: {
                min: 0,
                max: 100
              }
            }
          ]
        }
      },
      data: {
        labels: this.props.sentimentLabel,
        datasets: [{
          label: this.props.title,
          data: this.props.sentimentArray,
          backgroundColor: this.props.color
        }]
      }
    });
  }

  componentDidUpdate() {
    this.myChart.data.labels = this.props.sentimentLabel;
    this.myChart.data.datasets[0].data = this.props.sentimentArray;
    this.myChart.update();
  }

  render() {
      return <canvas ref={this.canvasRef} />
  }
}

// MAIN CLASS:

class FinSentiment extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      active: null,
      dataReceived: false,
      sentimentData: null,
      sentimentLabel: ["negative", "neutral", "positive"],
      sentimentArray: [0, 0, 0],
    };
    this.testSentiments = this.testSentiments.bind(this);
  };

  testSentiments() {
    axios.get('http://127.0.0.1:5000/test')
      .then((response) => {
        console.log(response);
        this.setState({sentimentData: response.data});
        this.setState({dataReceived: true});
        
        // Getting keys
        var keys = [];
        for (var k in response.data) keys.push(k);
        this.setState({sentimentLabel: keys});
        console.log(this.state.sentimentLabel);
        
        // Getting values
        var values = [];
        for (var j in response.data) values.push(response.data[j]);
        this.setState({sentimentArray: values});         
        console.log(this.state.sentimentArray);

      })
      .catch((error) => {
        console.log(error)
      })
  }

  render() {
    return (
    <div>
      <Button type='button' variant='success' onClick={this.testSentiments}>Test Sentiment</Button>
      <SentimentBarChart 
        dataReceived={this.state.dataReceived} 
        title="Sentiment Data" 
        color="#70CAD1" 
        sentimentLabel={this.state.sentimentLabel} 
        sentimentArray={this.state.sentimentArray}
      />
    </div>
    )
  }

};

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>Hung's NLP app</p>
        <FinSentiment/>
      </header>
    </div>
  );
}

export default App;