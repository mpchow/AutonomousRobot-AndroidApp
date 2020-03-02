package com.example.robotcontrol;

import android.graphics.BitmapFactory;
import android.os.Bundle;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.graphics.Bitmap;

import org.json.JSONObject;

import java.io.*;
import java.net.InetAddress;
import java.net.Socket;

public class MainActivity extends AppCompatActivity {

    private Socket socket;
    private BufferedInputStream in;
    private PrintWriter out;
    private InetAddress address; //Put address of the raspberry pi here
    private int port; //Put the port number of the raspberry pi here
    private ImageView robotCamera;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
//
//        FloatingActionButton fab = findViewById(R.id.fab);
//        fab.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View view) {
//                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
//                        .setAction("Action", null).show();
//            }
//        });

        final Button forwardButton = (Button) findViewById(R.id.forward);
        final Button backwardButton = (Button) findViewById(R.id.backwards);
        final Button leftButton = (Button) findViewById(R.id.leftwards);
        final Button rightButton = (Button) findViewById(R.id.rightwards);
        robotCamera = findViewById(R.id.imageView);

        forwardButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                moveForward();
            }
        });

        backwardButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                moveBackward();
            }
        });

        leftButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                turnLeft();
            }
        });


        rightButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                turnRight();
            }
        });


        try {
            serve();
        }
        catch (Exception e) {
            e.printStackTrace();
        }


    }


    public void serve() throws IOException{
        final TextView connectedStatus = (TextView) findViewById(R.id.textView);

        while (true) {
            try {
                //Connect it to the specified port and ip address
                socket = new Socket(address, port);
                //Setup the input and output streams
                in = new BufferedInputStream(socket.getInputStream());
//                in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                out = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));

                //If no exception, display a message so we know that it is connected
                connectedStatus.setText("Connected");

                mainFunctionality();
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                in.close();
                out.close();
                socket.close();
            }
        }
    }

    //Start to listen and serve requests
    public void mainFunctionality() {
        BitmapFactory converter = new BitmapFactory();
        while (true) {
            Bitmap image = converter.decodeStream(in);
            robotCamera.setImageBitmap(image);
        }
    }

    public void sendRequest(String movement) {
        JSONObject request = new JSONObject();
        try {
            request.put("Type", movement);
            out.print(request);
            out.flush();
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void receiveResponse() {

    }

    public void turnLeft()  {
        sendRequest("Left");
    }

    public void turnRight() {
        sendRequest("Right");
    }

    public void moveForward() {
        sendRequest("Forward");
    }

    public void moveBackward() {
        sendRequest("Backward");
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
