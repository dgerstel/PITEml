{
  // data file
  TFile * f = new TFile("../data/165527/VELODQM_165527_2015-10-12_18.55.28_NZS.root");

  const int lastSensorId = 41;
  TCanvas * cv = new TCanvas();

  TString sensorId;
  TString params; // [lastSensorId + 1];
  TString params_i;
  
  for (int i = 0; i <= lastSensorId; i++) {
    cv->Clear();
    
    // refresh default sensor name
    TString sensorName("TELL1_000");

    // set sensor name so it corresponds to the loop index
    sensorId.Form("%d", i);
    sensorName.Replace(sensorName.Sizeof() - sensorId.Sizeof(), sensorId.Sizeof(), sensorId);
    cout << sensorName << endl;

    // go to sensor's location
    if (!(f->cd("Vetra;1/VeloPedestalSubtractorMoni/" + sensorName + ";1"))) {
      cout << "Couldn't find sensor: " << sensorName << endl;
      break;
    }
    
    // draw its few graphs and save them
    // (1) 2D histogram
    Ped_Sub_ADCs_2D.Draw("colz");
    cv->SaveAs("../fig/" + sensorName + "_2D" + ".png");
    cv->Clear();
    // (2) 1D projection onto y-axis
    TH1D * noiseDistr = Ped_Sub_ADCs_2D.ProjectionY(); 
    noiseDistr->Draw();
    cv->SaveAs("../fig/" + sensorName + "_noiseDistr" + ".png");

    // get statistical params of the noise distribution
    double mu, sig, skew, kur, quality;
    mu = noiseDistr->GetMean();
    sig = noiseDistr->GetRMS();
    skew = noiseDistr->GetSkewness();
    kur = noiseDistr->GetKurtosis();

    // sensor quality 0 or 1 for now; [0.0, 100.0] in the future???
    quality = 1.0;

    cout << "Stat params {mu, sig, skewness, kurtosis} : " << mu << '\t' << sig << '\t' << skew << '\t' << kur << endl;

    params_i.Form("%f,%f,%f,%f,%f\n", mu, sig, skew, kur, quality);
    params.Append(params_i);
    cout << params;

  }
    //cout << params;
    ofstream myfile;
    myfile.open("../data/sensorData.dat");
    myfile << params;
    myfile.close();
    /*
    FILE * fout = fopen("../data/sensorData.dat", "w");
    //fprintf(fout, params);
    cout << params;
    printf(params);
    //&fout << params;
    //fprintf(fout, "%f,%f,%f,%f\n", mu, sig, skew, kur);
    fclose(fout);
    */

}
