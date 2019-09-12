package io.yashxd.esdlab1;


import android.os.Bundle;
//import android.support.v7.app.AppCompatActivity;
//import androidx.appcompat.R;

import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.FirebaseApp;
import com.google.firebase.database.ChildEventListener;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.util.ArrayList;
import java.util.List;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import static android.widget.Toast.LENGTH_LONG;

public class MainActivity extends AppCompatActivity implements AdapterView.OnItemSelectedListener{

    FirebaseDatabase database;
    DatabaseReference ref;

    volatile List<DataItem> dataItems = new ArrayList<>(0);
    volatile List<String> timeList = new ArrayList<String>(0);

    Spinner timeSpinner;
    Button fetchButton;
    Button switchButton;
    TextView currTemp;
    TextView currLight;
    TextView fetchedTemp;
    TextView fetchedLight;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        FirebaseApp.initializeApp(this);
        database = FirebaseDatabase.getInstance();
        ref = database.getReference("log");

        timeSpinner = (Spinner) findViewById(R.id.spinner_time);
        //fetchButton = (Button) findViewById(R.id.button_fetch);
        switchButton = (Button) findViewById(R.id.button_switch);
        currTemp = (TextView) findViewById(R.id.textview_curr_temp);
        currLight = (TextView) findViewById(R.id.textview_curr_light);
        fetchedTemp = (TextView) findViewById(R.id.textview_fetched_temp);
        fetchedLight = (TextView) findViewById(R.id.textview_fetched_light);

        fetchedTemp.setText("...");
        fetchedLight.setText(".|.");
        DataItem dataItem = new DataItem((int) (100*Math.random()) , (int) (1000*Math.random()), "time"+Math.random());
        String userId = ref.push().getKey();
        ref.child(userId).setValue(dataItem);

        final ArrayAdapter arrayAdapter = new ArrayAdapter(this, android.R.layout.simple_spinner_item, timeList);
        arrayAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        timeSpinner.setOnItemSelectedListener(this);
        timeSpinner.setAdapter(arrayAdapter);

        ref.addChildEventListener(new ChildEventListener() {
            @Override
            public void onChildAdded(@NonNull DataSnapshot dataSnapshot, @Nullable String s) {
                DataItem dataItem = dataSnapshot.getValue(DataItem.class);
                Log.v("DataItem retrieval", "onChildAdded " + dataItem.getTimeStamp());
                //Add the item to the starting of the data list
                dataItems.add(0,dataItem);
                timeList.add(0,dataItem.getTimeStamp());
                Toast.makeText(MainActivity.this,"Data added = "+dataItem.getTemp() + " at " + dataItem.getTimeStamp(),Toast.LENGTH_SHORT).show();
                currTemp.setText(""+dataItem.getTemp());
                currLight.setText(""+dataItem.getLight());
                arrayAdapter.notifyDataSetChanged();
                //arrayAdapter.clear();
                //arrayAdapter.add(timeList);
                //arrayAdapter.addAll(timeList);
            }

            @Override
            public void onChildChanged(@NonNull DataSnapshot dataSnapshot, @Nullable String s) {
                DataItem dataItem = dataSnapshot.getValue(DataItem.class);
                Log.v("DataItem retrieval", "onChildChanged " + dataItem.getTimeStamp());
                int dataItemIndex = dataItems.indexOf(dataItem);
                if(dataItemIndex > -1) {    //Exists in the list
                    dataItems.set(dataItemIndex,dataItem);
                    timeList.set(dataItemIndex,dataItem.getTimeStamp());
                    Toast.makeText(MainActivity.this,"Data changed = "+dataItem.getTemp() + " at " + dataItem.getTimeStamp(),Toast.LENGTH_SHORT).show();
                    arrayAdapter.notifyDataSetChanged();
                    //arrayAdapter.clear();
                    //arrayAdapter.addAll(timeList);
                }
            }

            @Override
            public void onChildRemoved(@NonNull DataSnapshot dataSnapshot) {
                DataItem dataItem = dataSnapshot.getValue(DataItem.class);
                Log.v("DataItem retrieval", "onChildRemoved " + dataItem.getTimeStamp());
                int dataItemIndex = dataItems.indexOf(dataItem);
                if(dataItemIndex > -1) {    //Exists in the list
                    dataItems.remove(dataItemIndex);
                    timeList.remove(dataItemIndex);
                    arrayAdapter.notifyDataSetChanged();
                }
            }

            @Override
            public void onChildMoved(@NonNull DataSnapshot dataSnapshot, @Nullable String s) {
                //Not needed
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {
                Log.v("DataItem retrieval", "Problem here!");
                Toast.makeText(getApplicationContext(),"Error while loading DataItems. Please try again later!", Toast.LENGTH_SHORT).show();
            }
        });

        switchButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                DataItem dataItem = new DataItem((int) (100*Math.random()) , (int) (1000*Math.random()), "time"+Math.random());
                String userId = ref.push().getKey();
                ref.child(userId).setValue(dataItem);
            }
        });
        /*ArrayAdapter<String> timeAdapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item);
        timeAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        timeSpinner.setAdapter(timeAdapter);*/
    }

    @Override
    public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
        fetchedTemp.setText(""+dataItems.get(position).getTemp());
        fetchedLight.setText(""+dataItems.get(position).getLight());
    }

    @Override
    public void onNothingSelected(AdapterView<?> parent) {

    }
}
