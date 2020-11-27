function getAttendanceForDay(day, data, IDs) {
  let IDList = [];
  let returnList = Array.from(Array(IDs.length), () => "A");
  for(var i = 0; i < IDs.length; i++) {
    IDList.push(IDs[i][0]);
  }
  for(var i = 0; i < data.length; i++) {
    if(0 <= Date.parse(data[i][0]) - Date.parse(day) && Date.parse(data[i][0]) - Date.parse(day) < 86400000) {
      returnList[IDList.indexOf(data[i][1])] = "P"; //IDList.indexOf(data[i][1]) is equal to the index of the student ID number, which we mark with P for Present
    }
  }
  return returnList;
}

function getPTPData(data, IDs) {
  let IDList = [];
  let returnList = Array.from(Array(IDs.length), () => " ");
  for(var i = 0; i < IDs.length; i++) {
    IDList.push(IDs[i][0]);
  }
  for(var i = 0; i < data.length; i++) {
    returnList[IDList.indexOf(data[i][0])] = "Y"; //IDList.indexOf(data[i][0]) is equal to the index of the student ID number, which we mark with Y for Yes
  }
  return returnList;
}

function getHoursForEvent(day, data, IDs, multiplier) {
  let IDList = [];
  let returnList = Array.from(Array(IDs.length), () => 0);
  for(var i = 0; i < IDs.length; i++) {
    IDList.push(IDs[i][0]);
  }
  for(var i = 0; i < data.length; i++) {
    if(0 <= Date.parse(data[i][0]) - Date.parse(day) && Date.parse(data[i][0]) - Date.parse(day) < 86400000) {
      returnList[IDList.indexOf(data[i][1])] = multiplier;
    }
  }
  return returnList;
}

function getHoursForVariableEvent(IDs, eventData){
  let IDList = [];
  let returnList = Array.from(Array(IDs.length), () => 0);
  for(var i = 0; i < IDs.length; i++) {
    IDList.push(IDs[i][0]);
  }
    for(var i = 0; i < eventData.length; i++) {
      returnList[IDList.indexOf(eventData[i][0])] = eventData[i][1];
  }
  return returnList;
}

function totalHours(data) {
  let returnList = [];
  for(var i = 0; i < data.length; i++) {
    let hours = 0;
    let events = 0;
    for(var j = 0; j < data[i].length; j++) {
      if(typeof(data[i][j]) == "number") {
        hours += data[i][j];
        if(data[i][j] > 0) {
          events++;
        }
      }
    }
    returnList.push(Math.round((hours+Number.EPSILON)*100)/100 + "H : " + parseInt(events) + "E");
  }
  return returnList;
}

function totalAttendance(data) {
  let returnList = [];
  for(var i = 0; i < data.length; i++) {
    let presents = 0, absents = 0;
    for(var j = 0; j < data[i].length; j++) {
      if(data[i][j] == "P") {
        presents++;
      } else if(data[i][j] == "A") {
        absents++;
      }
    }
    returnList.push(presents + "P : " + absents + "A : " + Math.round(10000 * presents / (presents + absents)) / 100 + "%");
  }
  return returnList;
}

function getEventHours(event) {
  const first = event.split(":")[0];
  if(first.indexOf(".") >= 0) {
    return parseFloat(first.match(/\d+/g)[0] + "." + first.match(/\d+/g)[1]);
  }
  return parseFloat(first.match(/\d+/g)[0]);
}

function selectForEvent(data, people) {
  let IDs = [];
  let considered = [];
  let returnList = [];
  for(var i = 0; i < data.length; i++) {
    IDs.push(data[i][0]);
  }
  for(var i = 0; i < people.length; i++) {
    if(!people[i][0]) { continue };
    const index = IDs.indexOf(people[i][0]);
    let meeting = data[index][7].indexOf("Y") >= 0 && data[index][8].indexOf("Y") >= 0;
    const last_name = data[index][1];
    const first_name = data[index][2];
    const v_hours = getEventHours(data[index][12]);
    const v_events = data[index][12].split(":")[1].match(/\d+/g)[0];
    if(meeting) {
      considered.push([people[i][0], last_name, first_name, v_hours, v_events, data[index][12]]);
    }
  }
  considered.sort(function(a, b) { return a[4] - b[4] });
  considered.sort(function(a, b) { return a[3] - b[3] });
  for(var i = 0; i < considered.length; i++) {
    returnList.push([considered[i][0], considered[i][1], considered[i][2], considered[i][5]]);
  }
  return returnList;
}

function returnMembers(data) {
  let members = [];
  for(var i = 0; i < data.length; i++) { 
    const v_hours = getEventHours(data[i][12]);
    const v_events = data[i][12].split(":")[1].match(/\d+/g)[0];
    if(!(data[i][7].indexOf("Y") >= 0 && data[i][8].indexOf("Y") >= 0 && v_hours >= 10 && v_events >= 0)) {
      members.push([data[i][0], data[i][1], data[i][2], data[i][7], data[i][8], v_hours, v_events]);
    }
  }
  return members;
}

function getIDs(idData, nameData){
  //let IDs = [];
  let eventNames = [];
  for(var x=0; x<nameData.length; x++){
    eventNames.push(nameData[x][0].toLowerCase());
  }
  let IDs = Array.from(Array(eventNames.length), () => "MISSING");
  /*for(var x=0; x<eventNames.length;x++){
    for(var y=0; y<idData.length; y++){
      var fullName = idData[y][2].concat(" "+idData[y][1]);
      if(eventNames[x].toLowerCase().localeCompare(fullName.toLowerCase())==0)
        IDs.push(idData[y][0]);
    }
  }*/
  for(var y=0; y<idData.length; y++){
      var fullName = idData[y][2].concat(" "+idData[y][1]);
      if(eventNames.indexOf(fullName.toLowerCase())>=0)
        IDs[eventNames.indexOf(fullName.toLowerCase())] = idData[y][0];
    }
  return IDs;
}
