package com.example.robotcontrol;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.os.Handler;
import android.os.StrictMode;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.ImageView;
import android.widget.Switch;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Timer;
import java.util.TimerTask;

public class MainActivity extends AppCompatActivity {

    private Socket socket; //Create the socket instance
    private InputStream in; //Create the inputstream
    private PrintWriter out; //output stream instance
    private InetAddress address; //Put address of the raspberry pi here
    private int port; //Put the port number of the raspberry pi here
    private ImageView robotCamera; //create the imageView instance
    private Switch modeToggle; //Create the switch
    private TextView modeStatus; //Create text to display the mode status
    private Handler mHandler = new Handler();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //Instantiate the port
        port = 5035;

        //Change the android policy to allow us to use network operations on the main thread
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        //Try creating an ip address
        try {
//            address = InetAddress.getByName("137.82.226.227");
            address = InetAddress.getByName("137.82.226.222");

        } catch (UnknownHostException e) {
            e.printStackTrace();
        }

        //Instantiate the mode toggle
        modeToggle = (Switch) findViewById(R.id.modeToggle);
        //Instantiate the mode status
        modeStatus = (TextView) findViewById(R.id.ModeStatus);
        //Get the forwardButton
        final Button forwardButton = (Button) findViewById(R.id.forward);
        //Get the leftButton
        final Button leftButton = (Button) findViewById(R.id.leftwards);
        //Get the rightbutton
        final Button rightButton = (Button) findViewById(R.id.rightwards);
        //Get the stopButton
        final Button stopButton = (Button) findViewById(R.id.stop);
        //Get the startButton
        final Button startButton = (Button) findViewById(R.id.Start);

        //Instantiate the imageView and set settings
        robotCamera = findViewById(R.id.imageView);
        robotCamera.setLayerType(View.LAYER_TYPE_SOFTWARE, null);
        robotCamera.setVisibility(View.VISIBLE);

        //Create onclick listener for the start button
        startButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //Send json to pi that we want to start in stop mode
                sendRequest("Null", "Stop");

                //Retrieve the photo to display
                mainFunctionality();
            }
        });

        //Add an event listener for the forwardsButton to call moveForward onclick
        forwardButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                moveForward();
            }
        });

        //Add an event listener for stopButton to call stop
        stopButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                stop();
            }
        });

        //Add an event listener for the leftButton to call turnLeft onclick
        leftButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                turnLeft();
            }
        });

        //Add an event listener for the rightButton to call turnRight onclick
        rightButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                turnRight();
            }
        });

        //Add an event listener for the toggle
        modeToggle.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                //If the switch is on set the text to remote control
                if(isChecked) {
                    modeStatus.setText("Mode:Remote Control");
                }
                //If the switch is off set the text to autonomous
                else {
                    modeStatus.setText("Mode:Autonomous");
                }
                //Make sure we update the pi with the mode
                ChangeMode(isChecked);
            }
        });

        //Call serve to connect to the pi
            try {
                serve();
            } catch (Exception e) {
                //If exception, print stack trace
                e.printStackTrace();
            }
    }

    //Start the sever
    public void serve() throws IOException{
        //Set the onscreen message to say that there is a good connection
        final TextView connectedStatus = (TextView) findViewById(R.id.textView);

        //While loop for handling until we close sockets
        try {
            //Connect it to the specified port and ipaddress
            socket = new Socket(address, port);
            System.out.println("CONNECTED");
            //Setup the input and output streams
            in = socket.getInputStream();
            out = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));

            //If no exception, display a message so we know that it is connected
            connectedStatus.setText("Connected");

        } catch (Exception e) {
            System.out.println("Not connected");
            //If execption, print stack trace
            e.printStackTrace();
        //Once the try catch finishes
        }
    }

    //Start to listen and serve requests
    public void mainFunctionality() {
        //Create a bitmapfactory options object
        BitmapFactory.Options options = new BitmapFactory.Options();
        //Set the scaling to value of 8
        options.inSampleSize = 8;
        //create a new bitmap
        Bitmap image = BitmapFactory.decodeStream(in, null, options);
        //set the image as the newly converted bitmap if the image is not null
        if (image != null) {
            robotCamera.setImageBitmap(image);
        }
    }

    //Send a request
    public void sendRequest(String movement, String mode) {
        //Create a new JSONObject
        JSONObject request = new JSONObject();

        //Try adding fields to the JSON
        try {
            request.put("Type", movement);
            request.put("Mode", mode);
            //Send the request out over the socket
            out.print(request);
            //Flush the socket
            out.flush();
        }
        catch (Exception e) {
            //If exception, print stack trace
            e.printStackTrace();
        }
    }

    //Tell the pi to change modes
    public void ChangeMode(boolean mode) {
        //If toggle is set to remote control send mode for remote
        if(mode) {
            sendRequest("NULL", "Remote");
        }
        //If toggle is set to autonomous send mode for autonomous
        else {
            sendRequest("NULL", "Autonomous");
        }
    }

    //send a request to turn left
    public void turnLeft()  {
        //if the mode is remote control then send request
        if(modeStatus.getText() == "Mode:Remote Control") {
            sendRequest("Left", "Remote");
        }
    }

    //send a request to turn right
    public void turnRight() {
        //if the mode is remote control then send request
        if(modeStatus.getText() == "Mode:Remote Control") {
            sendRequest("Right", "Remote");
        }
    }

    //send a request to move forwards
    public void moveForward() {
        //if the mode is remote control then send request
        if(modeStatus.getText() == "Mode:Remote Control") {
            sendRequest("Forward", "Remote");
        }
    }

    //send a request to stop
    public void stop() {
        //if the mode is remote control then send request
        if(modeStatus.getText() == "Mode:Remote Control") {
            sendRequest("Stop", "Remote");
        }
    }



    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
