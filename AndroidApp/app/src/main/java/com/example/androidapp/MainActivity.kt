package com.example.androidapp

import android.os.Bundle
import android.view.View
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.androidapp.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        binding = ActivityMainBinding.inflate(layoutInflater)
        val view = binding.root
        setContentView(view)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
        binding.button.setOnClickListener { calculatePrediction(it) }




    }
    fun calculatePrediction(view: View) {
        var year = 0.0; var km_driven = 0.0; var fuel = 0.0; var seller_type = 0.0; var transmission = 0.0;
        var owner2 = 0.0; var owner3 = 0.0; var owner4pls = 0.0; var ownerTest = 0.0;

        val yearIn = binding.editTextText.text.toString()
        if (yearIn.isNotEmpty()){ year = yearIn.toDouble() }

        val km_drivenIn = binding.editTextText2.text.toString()
        if (km_drivenIn.isNotEmpty()){ km_driven = km_drivenIn.toDouble() }

        val fuelIn = binding.spinner.selectedItem.toString()
        if (fuelIn == "Petrol") { fuel = 1.0 }

        val sellerIn = binding.spinner4.selectedItem.toString()
        if (sellerIn == "Individual") { seller_type = 1.0 }

        val transmissionIn = binding.spinner2.selectedItem.toString()
        if (transmissionIn == "Manual") {  transmission = 1.0 }

        val ownerIn = binding.spinner3.selectedItem.toString()
        if (ownerIn == "Second Owner") { owner2 = 1.0 }
        else if (ownerIn == "Third Owner") { owner3 = 1.0 }
        else if (ownerIn == "Fourth and Above Owner") { owner4pls = 1.0 }
        else if (ownerIn == "Test Drive Car") { ownerTest = 1.0 }

        val inputs = doubleArrayOf(year, km_driven, fuel, seller_type, transmission, owner2, owner3, owner4pls, ownerTest)
        val predict = CarPrediction.score(inputs).toInt()

        binding.textView.text = predict.toString()

    }

}