import logo from './logo.svg';
import tedi from './tedi.jpeg';
import { Button, Image, Header, Divider, Grid, Dropdown } from 'semantic-ui-react';
import './App.css';
import axios from 'axios';
import {useState,useEffect} from 'react';
import TimePicker from 'react-time-picker';
// import DateFnsUtils from '@date-io/date-fns'; // choose your lib
// import {
//   DatePicker,
//   TimePicker,
//   DateTimePicker,
//   MuiPickersUtilsProvider,
// } from '@material-ui/pickers';
function App() {
  const [treatStatus, setTreatStatus] = useState("waiting")
  const [pickle, setPickle] = useState({})
  const [selectedDate, handleDateChange] = useState(new Date());
  const [timeUser, setTimeUser] = useState('10:00');
  const [treatFrequency, setTreatFrequency] = useState('Today')
  useEffect(() => {
    axios.get('/getPickle').then(
      res => {
        setPickle(res.data)
      }
    ).catch(err => console.log(err))
  },[])

  const handleTreatClick = () => {
    setTreatStatus("dispensing")

    axios.post('/giveTreat',{id: 'success'}).then(
      res => {
        if (res.data.key == 'success') {
          setTreatStatus("dispensed")
        }else{
          setTreatStatus("problem")
        }
        }
    ).catch(err => {setTreatStatus("problem")})
  }

  const setNewPickle = (newPickleAPI) => {
    axios.post('/setPickle',newPickleAPI).then(
      res => {
        setPickle(res.data)
      }
    ).catch(err => console.log(err))
  }

  const handleDecrement = () => {
    const newPickle = {...pickle}
    if (newPickle["maxNumOfTreatsPerDay"] > 0){
      newPickle["maxNumOfTreatsPerDay"] -= 1
      setNewPickle(newPickle)
    }
    
    
  }
  const handleIncrement = () => {
    const newPickle = {...pickle}

    newPickle["maxNumOfTreatsPerDay"] += 1
    setNewPickle(newPickle)
    
  }
  const handleScheduleAdd = () => {
    const newPickle = {...pickle}
    const today = new Date()
    newPickle['scheduledDispenseTreats'].push({'time':timeUser,'freq':treatFrequency,'scheduledDate':[parseInt(today.getFullYear()),parseInt(today.getMonth()+1),parseInt(today.getDate())]})
    setNewPickle(newPickle)
  }
  const handleTreatFreqChange = (e, { value}) => setTreatFrequency(value)
  const handleRemoveTime = (e, {key}) => {
    const newPickle = {...pickle}
    newPickle['scheduledDispenseTreats'].splice(key,1)
    setNewPickle(newPickle)
  }
  const handleResetTreatClick = (e, {key}) => {
    const newPickle = {...pickle}
    newPickle["treatsGivenToday"] = 0
    setNewPickle(newPickle)
  }
  
  return (
    <div className="App">
      
      <header className="App-header">
        <Image src={tedi} size='medium' circular/>
        <Divider hidden/>
        { treatStatus=='dispensing' ?
          <Button 
            loading
            content="Give Tedi a Treat!"
          />
        :
          <Button 
            content="Give Tedi a Treat!"
            onClick={handleTreatClick}
          />
        }
        { treatStatus=='dispensed' ?
          <Header as="h2" inverted>She Got a Treat!</Header>
        :
          ''
        }
        { treatStatus=='problem' ?
          <Header as="h2" inverted>hmmm. There was a problem.</Header>
        :
          ''
        }
        <Divider/>
        <Header as='h1' textAlign='center' inverted>Max Treats Per Day</Header>
        <Grid verticalAlign='middle'>
        
        <Header as='h1' textAlign='center' inverted>
          <Button content="-" onClick={handleDecrement}/>
          {"  "+pickle["maxNumOfTreatsPerDay"]+"     "}
          <Button content="+" onClick={handleIncrement}/>
        </Header>
        </Grid>
        <Header as='h3' textAlign='center' inverted>Tedi can have {(pickle["maxNumOfTreatsPerDay"]-pickle["treatsGivenToday"])} more treats today</Header>
        <Divider hidden/>
        <Header as='h1' textAlign='center' inverted>Schedule a Treat</Header>
        <Grid relaxed>
            <Grid.Column width={25} color={'grey'} key={'grey'}>
              {/* <Header>               */}
              <TimePicker
                onChange={setTimeUser}
                value={timeUser}
                inverted
              />
              <Dropdown
                    inline
                    placeholder='Today'
                    //value={treatFrequency}
                    onChange={handleTreatFreqChange}
                    options={[{key:'Today',text:'Today',value:"Today"},{key:'Tomorrow',text:'Tomorrow',value:"Tomorrow"},{key:'Everyday',text:'Everyday',value:"Everyday"}]}
                  />
              {/* </Header> */}
              <Button content="Add" onClick={handleScheduleAdd}/>
            </Grid.Column>
            {/* <Grid.Column width={5} color={'grey'} key={'grey'}>

            </Grid.Column> */}
        </Grid>
        <Divider hidden/>
        <Header as='h1' textAlign='center' inverted>Scheduled Treats</Header>
        {typeof(pickle['scheduledDispenseTreats']) !== 'undefined' ? pickle['scheduledDispenseTreats'].length > 0 ?
        pickle['scheduledDispenseTreats'].map((itm, i) => (
          
          <Header as='h2' inverted>
            {itm.time} {itm.freq}
            <Button content="Remove" key={i} onClick={handleRemoveTime}/>
          </Header>
        ))
      :'':''}
        <Divider hidden/>
        <Button 
            content="Reset Todays Treats to 0"
            onClick={handleResetTreatClick}
          />
        </header>
      

    </div>
  );
}

export default App;
