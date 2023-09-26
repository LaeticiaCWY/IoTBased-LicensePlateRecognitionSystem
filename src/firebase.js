// src/firebase.js
import firebase from 'firebase/compat/app'; // Import Firebase app
import 'firebase/compat/storage'; // Import Firebase storage
import 'firebase/compat/database'; 

const firebaseConfig = {
  apiKey: 'AIzaSyAZfHF22hO29tzwfGbh8mroC69Z7Qbfk1o',
  authDomain: 'lpr1-2a779.firebaseapp.com',
  databaseURL: 'https://lpr1-2a779-default-rtdb.asia-southeast1.firebasedatabase.app',
  projectId: 'lpr1-2a779',
  storageBucket: 'lpr1-2a779.appspot.com',
  messagingSenderId: '759846216195',
  appId: '1:759846216195:web:c69c70bf769766b2b9e436',
  measurementId: 'G-F283Z4ZW7T',
};


firebase.initializeApp(firebaseConfig);
const storage = firebase.storage();
const database = firebase.database();

export { storage, database, firebase };