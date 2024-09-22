<h1>N1 - Web Library with Flask</h1>
<p>It's a simple website developed with pure Python (API), HTML and CSS (design) in order to learn how API's works; Was proposed as test (N1 = first grade), consisting in one of three notes we've the semester of software engineering degree of Católica University in Jaraguá do Sul, Brazil.</p>

<h2>What's the scope and its limitations?</h2>
<p>For grade N1, we will create user management and a login screen (without using JWT tokens).</p>

<p>You will need to implement:</p>

<ol>
  <li>Database Table(initdb should create the user table):
    <ol>
      <li>The user table should have the following fields: 
        <ul>
          <li><code>id;</code></li>
          <li><code>login</code> (must be the email);</li>
          <li><code>password</code>;</li>
          <li><code>real name</code>;</li>
          <li><code>user creation date</code>;</li>
          <li><code>status</code> (active/blocked);</li>
          <li><code>last update date</code> of the user.</li>
        </ul>
      </li>
    </ol>
  </li>

  <li>Create endpoints to perform <strong>CRUD</strong> operations on the table:
    <ol style="list-style-type: upper-alpha;">
      <li>When creating the user, the password must be encrypted using a one-way method (it should not be possible to decrypt the password);</li>
      <li><strong>It should NOT</strong> be allowed to create users with the same login. When registering, data validation should occur. This validation can happen at the time of data submission, there's no need to validate when leaving the field;</li>
      <li>When registering the user, validation of the login should occur to ensure that the chosen login is an email;</li>
      <li>When creating the user, the user creation date should be filled with the current date;</li>
      <li>When making any changes to the user, the last update date should be filled with the date of the record change (the creation date should remain unchanged);</li>
      <li>Users <strong>CANNOT</strong> be deleted, only blocked.</li>
    </ol>
  </li>

  <li>Create a template for user management (the CRUD operations above should be done via a graphical interface):
    <ol style="list-style-type: upper-alpha;">
      <li>Remember that "deletion" will only mark the user as blocked.</li>
    </ol>
  </li>

  <li>Create a login screen template, so that the user can access the system. It should be available at an endpoint <code>/login</code>, and accessible from the top navigation bar of the service:
    <ol style="list-style-type: upper-alpha;">
      <li>If the user is blocked, <strong>login should not be allowed.</strong> A message should be displayed on the screen informing the user of the fact;</li>
      <li>If the user is successfully authenticated (login and password are correct), the user should be redirected to a homepage (of your choice);</li>
      <li>For now, other endpoints can be accessed directly, <strong>routes will not be protected</strong> at this stage of the assignment.</li>
    </ol>
  </li>
</ol>

<h2>Project Setup</h2>
<p>We need a few things to run this simple project, that are:</p>
<ol>
    <li>Download VScode IDE if you don't have installed;</li>
    <li>Install <a href="https://www.python.org/downloads/">Python</a> last version or above 3.0 and reboot your pc;</li>
    <li>Install <a href="https://dev.to/dendihandian/installing-sqlite3-in-windows-44eb">SQLite3</a> last version or above 3.40.0 and reboot your pc;</li>
    <li>Download the project .zip or clone it with GitHub, extract all folders in one folder of your choice in your PC;</li>
    <li>Inside VScode with the project folder open, click <code>CTRL + SHIFT + `</code> or type in VScode search bar <code>>Terminal: create new terminal</code> and press <code>Enter</code>;</li>
    <li>With terminal open, install this libraries using the syntax below, just copy and paste in terminal:
        <ol ol style="list-style-type: upper-alpha;">
            <li><code>pip install flask</code></li>
            <li><code>pip install bcrypt</code></li>
            <li><code>pip install pysqlite3</code></li>
        </ol>
    </li>
    <li>Now, just open <code>main.py</code> and run it with, to run the server you can use two methods:
        <ol ol style="list-style-type: upper-alpha;">
            <li>You can install the VScode extension <a href="https://marketplace.visualstudio.com/items?itemName=formulahendry.code-runner">Code Runner</a>, with the file open and extension installed, use shortcut <code>Ctrl + Alt + N</code> to run;</li>
            <li>In the terminal, make sure you are in the right directory and then type: <code>python main.py</code> to start server;</li>
        </ol>
    </li>
    <li>The server/application already have a database file with some data (<code>database.db</code>), but if you want to start from zero, exclude <code>database.db</code> file and then access the route <code>/initdb</code> to create a new one with all tables and no data inside;</li>
    <li>Enjoy exploring!</li>
</ol>