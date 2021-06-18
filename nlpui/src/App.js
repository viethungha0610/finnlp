import './App.css';
import React from 'react';
import axios from 'axios';
import {Button, Spinner} from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import Chart from 'chart.js/auto';
import MaterialTable from '@material-table/core';

// BAR CHART!

const columns = [
  {
    title: "Timestamp",
    field: "Timestamp",
  },
  {
    title: "Source",
    field: "Source",
  },
  {
    title: "Headline",
    field: "Headline",
  },
  {
    title: "Sentiment",
    field: "Sentiment",
  },
];

function DataTable(props) {
  if (props.tableReceived) {
    return (
      <MaterialTable 
        data={props.data} 
        columns={columns} 
        options={{ 
          search: true, 
          paging: true, 
          filtering: true, 
          exportButton: true, 
          rowStyle: {
            fontSize: 12,
        },
          headerStyle: {
            fontSize: 12,
        },
          style: {
            fontSize: 12,
          }
      }}
        />
    )
  }
  else {
    return null;
  }
}

function SpinningWheel(props) {
  if (props.loading) {
    return (
      <div>
        <div>Scraping data and analyzing sentiments ...</div>
        <Spinner animation="border" variant="primary" />
      </div>
    )
  }
  else {
    return null;
  }
}

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
      loading: false,
      tableReceived: false,
      dataTable: null,
    };
    this.testSentiments = this.testSentiments.bind(this);
    this.testTable = this.testTable.bind(this);
  };

  testTable() {
    axios.get('http://127.0.0.1:5000/datatable')
      .then((response) => {
        console.log(response);
        this.setState({dataTable: response.data});
        this.setState({tableReceived: true});
      })
      .catch((error) => {
        console.log(error);
      })
  }

  testSentiments() {
    this.setState({loading: true});
    axios.get('http://127.0.0.1:5000/sentiments')
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

        this.setState({loading: false});

      })
      .catch((error) => {
        console.log(error);
        this.setState({loading: false});
      })
  }

  render() {
    return (
    <div class="row">
      <div class="column">
        <Button type='button' variant='success' onClick={this.testSentiments}>Test Sentiment</Button>
        <SpinningWheel loading={this.state.loading} />
        <SentimentBarChart 
          dataReceived={this.state.dataReceived} 
          title="Sentiment Data" 
          color="#70CAD1" 
          sentimentLabel={this.state.sentimentLabel} 
          sentimentArray={this.state.sentimentArray}
        />
      </div>
      <div class="column">
        <Button type='button' variant='success' onClick={this.testTable}>Test Data Table</Button>
        <DataTable data={this.state.dataTable} tableReceived={this.state.tableReceived} />
      </div>
    </div>
    )
  }

};

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>Hung's NLP Web App (in development)</p>
        <FinSentiment/>
      </header>
    </div>
  );
}

export default App;