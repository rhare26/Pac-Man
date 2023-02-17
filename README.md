<h1>Pac-Man</h1>
<h3>Description</h3>
    This project is a recreation of the classic Pac-Man game. It includes a maze for a player to navigate through using arrow keys or a joystick. The player is chased by up to four ghosts. Fruits and energizers (along with vulnerable ghosts) are also included.

<h3>Hardware</h3>
    <ul>
        <li>4gb Pi 4</li>
        <li>Optional: EG STARTS joystick</li>
        <li>Optional: EG STARTS joystick controller (optional)</li>
        <li>Optional: 4 EG STARTS buttons (optional)</li>
    </ul>
<h3>Install</h3>
    <ol>
        <li>Install python 3.9.2</li>
        <li>````pip3 install -r requirements.txt````</li>
        <li>If receiving errors about bmps, SDl, ttf, fonts, or other, try:<br>
    ````sudo apt install python-dev libsdl-image1.2-dev libsdl-ttf2.0-dev libfreetype6-dev````
        <li>Optional: Attach buttons to respective ports on joystick controller: 
            <ul>
                <li>Menu/Blue = 0</li>
                <li>New/Green = 1</li>
                <li>Continue/Yellow = 2</li>
            </ul>
        <li>Optional: Plug joystick controller into Raspberry Pi via USB port
    </ol>