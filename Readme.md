# Hi there 👋👋
## Octagon🛑
The project Octagon is a final year academic project. <br>
Octagon supports eight functionalities:<b>
  - Face Verification, 
  - Post Attendence, 
  - Managing Attendance, 
  - Analysing Attendance, 
  - Managing Timetable, 
  - View Teacher Hours, 
  - Department Statistics,
  - University Notification</b>.
  
<p align="center">
  Octagon has three modules: Admin, Hod, and Teacher.<br>
  <br>
  <img src="https://user-images.githubusercontent.com/58617251/166411113-41945bb0-65a1-4a08-bb15-3dad60bcbaa0.png" width="600" height="350">
</p>

### Data Flow Diagrams

<table>

  <tr>
    <td><img src="https://user-images.githubusercontent.com/58617251/166411650-63a38767-e602-4692-bef7-1ea8059b42ab.png"></td>
    <td><img src="https://user-images.githubusercontent.com/58617251/166411658-1535cab8-fb30-4671-8e0d-51c66a964378.png"></td>
  </tr>
  
  <tr>
    <td colspan=2>
       <p align="center">
         <img src="https://user-images.githubusercontent.com/58617251/166411069-5a6a46e9-5543-45e7-9887-e4a548aacb4b.png" align="center" width="auto" height="350">
      </p>
     </td>
  </tr>
</table>


### Application ScreenShots


<table>
  <tr>
    <td>
      <img src="https://user-images.githubusercontent.com/58617251/166414363-be698e6b-f818-48c5-86ea-6af1437edcb2.png">
    </td>
    <td>
      <img src="https://user-images.githubusercontent.com/58617251/166414433-ff417bea-6036-48c3-a2d8-43c38548ec22.png">
    </td>
  </tr>
  
  <tr>
    <td>
     <img src="https://user-images.githubusercontent.com/58617251/166416344-6db686e3-6950-4979-b02f-d08c64fa02e1.png">
    </td>
    <td>
      <img src="https://user-images.githubusercontent.com/58617251/166416352-a130ebad-b428-490b-a91c-160c97afee34.png">
    </td>
  </tr>
  
  <tr>  
    <td>
      <img src="https://user-images.githubusercontent.com/58617251/166416377-45ef275f-f328-441b-9833-343708fd759b.png">
    </td>
    <td>
      <img src="https://user-images.githubusercontent.com/58617251/166417113-8ed5c943-d0c7-493f-9f8f-f615c164f7f9.png">
    </td>
  </tr>
</table>



### To Run Application

#### Build Docker

* docker build -t octagon .

#### Run Docker

* docker run -d -p 80:80 octagon
